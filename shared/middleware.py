"""
Security middleware — API key authentication.

Every request is blocked unless it carries a valid X-API-Key header.
The only public endpoint is /.well-known/agent-card.json.
"""
import json
import logging
import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from shared.fhir_hook import extract_fhir_from_payload
from shared.logging_utils import redact_headers, safe_pretty_json, token_fingerprint

logger = logging.getLogger(__name__)

LOG_FULL_PAYLOAD = os.getenv("LOG_FULL_PAYLOAD", "true").lower() == "true"

# Load API keys from environment. Fall back to a dev key for local testing.
VALID_API_KEYS: set = {
    k for k in [
        os.getenv("HOMEWARD_API_KEY"),
    ]
    if k
} or {"homeward-dev-key-123"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that enforces X-API-Key authentication
    and bridges FHIR metadata from message.metadata to params.metadata.
    """

    async def dispatch(self, request: Request, call_next):
        body_bytes = await request.body()
        body_text  = body_bytes.decode("utf-8", errors="replace")
        parsed     = {}
        try:
            parsed      = json.loads(body_text) if body_text else {}
            pretty_body = safe_pretty_json(parsed)
        except json.JSONDecodeError:
            pretty_body = body_text

        if LOG_FULL_PAYLOAD:
            logger.info(
                "incoming_http_request path=%s method=%s headers=%s\npayload=\n%s",
                request.url.path, request.method,
                safe_pretty_json(redact_headers(dict(request.headers))),
                pretty_body,
            )

        # Rewrite Prompt Opinion's PascalCase JSON-RPC methods to A2A spec form.
        # PO sends SendMessage / SendStreamingMessage; a2a-sdk expects message/send / message/stream.
        method_map = {
            "SendMessage": "message/send",
            "SendStreamingMessage": "message/stream",
            "GetTask": "tasks/get",
            "CancelTask": "tasks/cancel",
        }
        if isinstance(parsed, dict) and parsed.get("method") in method_map:
            original = parsed["method"]
            parsed["method"] = method_map[original]
            logger.info("METHOD_REWRITTEN from=%s to=%s", original, parsed["method"])

        # Normalise PO's proto-style enums to A2A spec lowercase forms.
        # role: ROLE_USER -> user, ROLE_AGENT -> agent
        # part type: TEXT -> text (in case PO sends it)
        role_map = {"ROLE_USER": "user", "ROLE_AGENT": "agent"}
        try:
            msg = parsed.get("params", {}).get("message")
            if isinstance(msg, dict):
                if msg.get("role") in role_map:
                    msg["role"] = role_map[msg["role"]]
                    logger.info("ROLE_NORMALISED to=%s", msg["role"])
                for part in msg.get("parts", []) or []:
                    if isinstance(part, dict):
                        kind = part.get("kind") or part.get("type")
                        if isinstance(kind, str) and kind.isupper():
                            part["kind"] = kind.lower()
        except (AttributeError, TypeError):
            pass

        # Re-serialise once after all rewrites
        if isinstance(parsed, dict) and parsed:
            body_bytes = json.dumps(parsed, ensure_ascii=False).encode("utf-8")
            request._body = body_bytes

        # Bridge FHIR metadata
        fhir_key, fhir_data = extract_fhir_from_payload(parsed)
        if isinstance(parsed, dict):
            params = parsed.get("params")
            if isinstance(params, dict):
                if fhir_key and fhir_data and not params.get("metadata"):
                    params["metadata"] = {fhir_key: fhir_data}
                    body_bytes = json.dumps(parsed, ensure_ascii=False).encode("utf-8")
                    request._body = body_bytes
                    logger.info(
                        "FHIR_METADATA_BRIDGED source=message.metadata target=params.metadata key=%s",
                        fhir_key,
                    )
                if fhir_data:
                    logger.info("FHIR_URL_FOUND value=%s",         fhir_data.get("fhirUrl", "[EMPTY]"))
                    logger.info("FHIR_TOKEN_FOUND fingerprint=%s", token_fingerprint(fhir_data.get("fhirToken", "")))
                    logger.info("FHIR_PATIENT_FOUND value=%s",     fhir_data.get("patientId", "[EMPTY]"))
                else:
                    logger.info("FHIR_NOT_FOUND_IN_PAYLOAD keys_checked=params.metadata,message.metadata")

        # Agent card is always public — also patch in supportedInterfaces
        # (required by Prompt Opinion's parser, not emitted by current a2a-sdk).
        if request.url.path == "/.well-known/agent-card.json":
            response = await call_next(request)
            try:
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                card = json.loads(body.decode("utf-8"))
                base_url = card.get("url") or ""
                # supportedInterfaces — Prompt Opinion / A2A v1 format
                card["supportedInterfaces"] = [
                    {
                        "url": base_url,
                        "protocolBinding": "JSONRPC",
                        "protocolVersion": "1.0",
                    }
                ]
                card["preferredTransport"] = "JSONRPC"
                card["protocolVersion"] = "1.0"
                # securitySchemes — A2A v1 nested-key format expected by PO
                if card.get("securitySchemes"):
                    card["securitySchemes"] = {
                        "apiKey": {
                            "apiKeySecurityScheme": {
                                "name": "X-API-Key",
                                "location": "header",
                                "description": "API key required to access this agent.",
                            }
                        }
                    }
                    card["security"] = [{"apiKey": []}]
                new_body = json.dumps(card).encode("utf-8")
                return JSONResponse(
                    content=card,
                    status_code=response.status_code,
                    headers={"content-type": "application/json"},
                )
            except Exception as e:
                logger.warning("agent_card_patch_failed error=%s — serving original", e)
                return JSONResponse(
                    content=json.loads(body.decode("utf-8")) if body else {},
                    status_code=response.status_code,
                )

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            logger.warning(
                "security_rejected_missing_api_key path=%s method=%s",
                request.url.path, request.method,
            )
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "detail": "X-API-Key header is required"},
            )

        if api_key not in VALID_API_KEYS:
            logger.warning(
                "security_rejected_invalid_api_key path=%s method=%s key_prefix=%s",
                request.url.path, request.method, api_key[:6],
            )
            return JSONResponse(
                status_code=403,
                content={"error": "Forbidden", "detail": "Invalid API key"},
            )

        logger.info(
            "security_authorized path=%s method=%s key_prefix=%s",
            request.url.path, request.method, api_key[:6],
        )

        # Capture response so we can log it AND wrap Message-shaped results as Tasks
        # (Prompt Opinion's external-agent client requires a Task envelope).
        response = await call_next(request)
        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            text = body.decode("utf-8", errors="replace")
            logger.info("outgoing_response status=%s body=\n%s", response.status_code, text[:4000])

            data = json.loads(text)
            result = data.get("result") if isinstance(data, dict) else None

            if isinstance(result, dict):
                logger.info("RESPONSE_FIXUP_ENTERED keys=%s", list(result.keys()))
                import uuid as _uuid

                # A2A v1 specification — no `kind` discriminators on Task/Message/Part.
                result.pop("kind", None)

                def _strip_kind_from_parts(parts: list) -> list:
                    out = []
                    for p in parts or []:
                        if isinstance(p, dict):
                            out.append({k: v for k, v in p.items() if k != "kind"})
                        else:
                            out.append(p)
                    return out

                # Promote a bare Message-at-root to an artifact.
                if "parts" in result and "artifacts" not in result:
                    result_parts = result.pop("parts", [])
                    result["artifacts"] = [{
                        "artifactId": str(_uuid.uuid4()),
                        "name": "response",
                        "parts": _strip_kind_from_parts(result_parts),
                    }]

                for art in result.get("artifacts", []) or []:
                    if isinstance(art, dict):
                        art.pop("kind", None)
                        art["parts"] = _strip_kind_from_parts(art.get("parts", []))

                for msg in result.get("history", []) or []:
                    if isinstance(msg, dict):
                        msg.pop("kind", None)
                        msg["parts"] = _strip_kind_from_parts(msg.get("parts", []))

                # Required Task fields per spec: id, status. Add if missing.
                if "taskId" in result and "id" not in result:
                    result["id"] = result["taskId"]
                if "id" not in result:
                    result["id"] = str(_uuid.uuid4())
                if "contextId" not in result:
                    result["contextId"] = str(_uuid.uuid4())

                # status.state — PO uses proto enums (ROLE_USER, SendMessage) so try
                # the proto-style TASK_STATE_COMPLETED form for state too.
                proto_state_map = {
                    "completed":      "TASK_STATE_COMPLETED",
                    "submitted":      "TASK_STATE_SUBMITTED",
                    "working":        "TASK_STATE_WORKING",
                    "input-required": "TASK_STATE_INPUT_REQUIRED",
                    "canceled":       "TASK_STATE_CANCELED",
                    "failed":         "TASK_STATE_FAILED",
                    "rejected":       "TASK_STATE_REJECTED",
                    "auth-required":  "TASK_STATE_AUTH_REQUIRED",
                }
                status = result.get("status") if isinstance(result.get("status"), dict) else {}
                state = status.get("state", "completed")
                if not state.startswith("TASK_STATE_"):
                    state = proto_state_map.get(state, "TASK_STATE_COMPLETED")
                status["state"] = state
                result["status"] = status

                # role on history messages → proto form
                role_map_proto = {"user": "ROLE_USER", "agent": "ROLE_AGENT"}
                for msg in result.get("history", []) or []:
                    if isinstance(msg, dict) and msg.get("role") in role_map_proto:
                        msg["role"] = role_map_proto[msg["role"]]

                # PO checks $.result.task — wrap the Task under a "task" key per
                # the A2A v1 specification's REST-style response shape.
                data["result"] = {"task": result}
                final_body = json.dumps(data)
                logger.info("FINAL_WIRE_BODY=%s", final_body[:4000])
                return JSONResponse(content=data, status_code=response.status_code)
        except Exception as e:
            logger.warning("response_wrap_failed error=%s — serving original", e)

        return JSONResponse(
            content=json.loads(body.decode("utf-8")) if body else {},
            status_code=response.status_code,
            headers={"content-type": "application/json"},
        )
