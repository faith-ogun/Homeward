"""
FHIR tools — query a FHIR R4 server on behalf of the patient in context.

These tools read FHIR credentials (fhir_url, fhir_token, patient_id) from
tool_context.state — values injected by fhir_hook.extract_fhir_context.
"""
import logging

import httpx
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

_FHIR_TIMEOUT = 15


def _get_fhir_context(tool_context: ToolContext):
    """Read FHIR credentials from session state. Returns tuple or error dict."""
    fhir_url   = tool_context.state.get("fhir_url",   "").rstrip("/")
    fhir_token = tool_context.state.get("fhir_token", "")
    patient_id = tool_context.state.get("patient_id", "")

    missing = [
        name for name, val in [
            ("fhir_url",   fhir_url),
            ("fhir_token", fhir_token),
            ("patient_id", patient_id),
        ]
        if not val
    ]
    if missing:
        return {
            "status": "error",
            "error_message": (
                f"FHIR context is not available — missing: {', '.join(missing)}. "
                "Ensure the caller includes 'fhir-context' in the A2A message metadata."
            ),
        }
    return fhir_url, fhir_token, patient_id


def _fhir_get(fhir_url: str, token: str, path: str, params: dict | None = None) -> dict:
    """Perform an authenticated FHIR GET and return the parsed JSON response."""
    response = httpx.get(
        f"{fhir_url}/{path}",
        params=params,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept":        "application/fhir+json",
        },
        timeout=_FHIR_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _http_error_result(exc: httpx.HTTPStatusError) -> dict:
    return {
        "status":        "error",
        "http_status":   exc.response.status_code,
        "error_message": f"FHIR server returned HTTP {exc.response.status_code}: {exc.response.text[:200]}",
    }


def _connection_error_result(exc: Exception) -> dict:
    return {
        "status":        "error",
        "error_message": f"Could not reach FHIR server: {exc}",
    }


def _coding_display(codings: list) -> str:
    """Return the first human-readable display text from a list of FHIR codings."""
    for c in codings:
        if c.get("display"):
            return c["display"]
    return "Unknown"


def get_patient_demographics(tool_context: ToolContext) -> dict:
    """
    Fetches the demographic information for the current patient from the FHIR server.

    Returns name, date of birth, gender, and primary contact details.
    No arguments required — the patient identity comes from the session context.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    logger.info("tool_get_patient_demographics patient_id=%s", patient_id)
    try:
        patient = _fhir_get(fhir_url, fhir_token, f"Patient/{patient_id}")
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    names    = patient.get("name", [])
    official = next((n for n in names if n.get("use") == "official"), names[0] if names else {})
    given    = " ".join(official.get("given", []))
    family   = official.get("family", "")
    full_name = f"{given} {family}".strip() or "Unknown"

    contacts = [
        {"system": t.get("system"), "value": t.get("value"), "use": t.get("use")}
        for t in patient.get("telecom", [])
    ]

    addrs   = patient.get("address", [])
    address = None
    if addrs:
        a = addrs[0]
        address = ", ".join(filter(None, [
            " ".join(a.get("line", [])),
            a.get("city"), a.get("state"), a.get("postalCode"), a.get("country"),
        ]))

    return {
        "status":         "success",
        "patient_id":     patient_id,
        "name":           full_name,
        "birth_date":     patient.get("birthDate"),
        "gender":         patient.get("gender"),
        "active":         patient.get("active"),
        "contacts":       contacts,
        "address":        address,
        "marital_status": (patient.get("maritalStatus") or {}).get("text"),
    }


def get_active_medications(tool_context: ToolContext) -> dict:
    """
    Retrieves the patient's current active medication list from the FHIR server.

    Queries MedicationRequest resources with status=active and returns medication
    names, dosage instructions, and prescribing dates.
    No arguments required.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    logger.info("tool_get_active_medications patient_id=%s", patient_id)
    try:
        bundle = _fhir_get(
            fhir_url, fhir_token, "MedicationRequest",
            params={"patient": patient_id, "status": "active", "_count": "50"},
        )
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    medications = []
    for entry in bundle.get("entry", []):
        res         = entry.get("resource", {})
        med_concept = res.get("medicationCodeableConcept", {})
        med_name    = (
            med_concept.get("text")
            or _coding_display(med_concept.get("coding", []))
            or res.get("medicationReference", {}).get("display", "Unknown")
        )
        dosage_list = [d.get("text", "No dosage text") for d in res.get("dosageInstruction", [])]
        medications.append({
            "medication":  med_name,
            "status":      res.get("status"),
            "dosage":      dosage_list[0] if dosage_list else "Not specified",
            "authored_on": res.get("authoredOn"),
            "requester":   (res.get("requester") or {}).get("display"),
        })

    return {
        "status":      "success",
        "patient_id":  patient_id,
        "count":       len(medications),
        "medications": medications,
    }


def get_active_conditions(tool_context: ToolContext) -> dict:
    """
    Retrieves the patient's active conditions and diagnoses from the FHIR server.

    Queries Condition resources with clinical-status=active and returns the
    problem list with condition names, severity, and onset dates.
    No arguments required.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    logger.info("tool_get_active_conditions patient_id=%s", patient_id)
    try:
        bundle = _fhir_get(
            fhir_url, fhir_token, "Condition",
            params={"patient": patient_id, "clinical-status": "active", "_count": "50"},
        )
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    conditions = []
    for entry in bundle.get("entry", []):
        res   = entry.get("resource", {})
        code  = res.get("code", {})
        onset = res.get("onsetDateTime") or (res.get("onsetPeriod") or {}).get("start")
        conditions.append({
            "condition":       code.get("text") or _coding_display(code.get("coding", [])),
            "clinical_status": (
                (res.get("clinicalStatus") or {}).get("coding", [{}])[0].get("code")
            ),
            "severity":        (res.get("severity") or {}).get("text"),
            "onset":           onset,
            "recorded_date":   res.get("recordedDate"),
        })

    return {
        "status":     "success",
        "patient_id": patient_id,
        "count":      len(conditions),
        "conditions": conditions,
    }


def get_recent_observations(category: str, tool_context: ToolContext) -> dict:
    """
    Retrieves recent clinical observations for the patient from the FHIR server.

    Args:
        category: FHIR observation category. Common values:
                    'vital-signs'    — blood pressure, heart rate, temperature, SpO2
                    'laboratory'     — lab results (CBC, HbA1c, metabolic panel, etc.)
                    'social-history' — smoking status, alcohol use, etc.
                  Defaults to 'vital-signs' if not specified.

    Returns the 20 most recent observations in the category, newest first.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    category = (category or "vital-signs").strip().lower()
    logger.info("tool_get_recent_observations patient_id=%s category=%s", patient_id, category)
    try:
        bundle = _fhir_get(
            fhir_url, fhir_token, "Observation",
            params={"patient": patient_id, "category": category, "_sort": "-date", "_count": "20"},
        )
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    observations = []
    for entry in bundle.get("entry", []):
        res  = entry.get("resource", {})
        code = res.get("code", {})
        obs_name = code.get("text") or _coding_display(code.get("coding", []))

        value, unit = None, None
        if "valueQuantity" in res:
            vq    = res["valueQuantity"]
            value = vq.get("value")
            unit  = vq.get("unit") or vq.get("code")
        elif "valueCodeableConcept" in res:
            value = (res["valueCodeableConcept"].get("text")
                     or _coding_display(res["valueCodeableConcept"].get("coding", [])))
        elif "valueString" in res:
            value = res["valueString"]

        components = []
        for comp in res.get("component", []):
            comp_code = (comp.get("code") or {})
            comp_name = comp_code.get("text") or _coding_display(comp_code.get("coding", []))
            comp_vq   = comp.get("valueQuantity", {})
            components.append({
                "name":  comp_name,
                "value": comp_vq.get("value"),
                "unit":  comp_vq.get("unit") or comp_vq.get("code"),
            })

        observations.append({
            "observation":    obs_name,
            "value":          value,
            "unit":           unit,
            "components":     components or None,
            "effective_date": res.get("effectiveDateTime") or (res.get("effectivePeriod") or {}).get("start"),
            "status":         res.get("status"),
            "interpretation": (
                (res.get("interpretation") or [{}])[0].get("text")
                or _coding_display((res.get("interpretation") or [{}])[0].get("coding", []))
            ),
        })

    return {
        "status":       "success",
        "patient_id":   patient_id,
        "category":     category,
        "count":        len(observations),
        "observations": observations,
    }


def get_procedures(tool_context: ToolContext) -> dict:
    """
    Retrieves the patient's procedures from the FHIR server.

    Returns each procedure with its display name, performed date, and reason.
    Used to determine which surgical procedure the patient had and when, so
    Homeward can compute post-operative day and look up the recovery timeline.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    logger.info("tool_get_procedures patient_id=%s", patient_id)
    try:
        bundle = _fhir_get(
            fhir_url, fhir_token, "Procedure",
            params={"patient": patient_id, "_count": "20", "_sort": "-date"},
        )
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    procedures = []
    for entry in bundle.get("entry", []):
        res  = entry.get("resource", {})
        code = res.get("code", {})
        performed = (
            res.get("performedDateTime")
            or (res.get("performedPeriod") or {}).get("start")
        )
        reasons = [r.get("text") for r in res.get("reasonCode", []) if r.get("text")]
        procedures.append({
            "procedure":      code.get("text") or _coding_display(code.get("coding", [])),
            "snomed_codes":   [c.get("code") for c in code.get("coding", []) if c.get("code")],
            "performed_date": performed,
            "status":         res.get("status"),
            "reason":         "; ".join(reasons) if reasons else None,
        })

    return {
        "status":     "success",
        "patient_id": patient_id,
        "count":      len(procedures),
        "procedures": procedures,
    }


def get_pgx_panel(tool_context: ToolContext) -> dict:
    """
    Retrieves pharmacogenomic (PGx) panel results for the patient from the FHIR server.

    Queries DiagnosticReport resources in the genetics category and returns the
    diplotype/phenotype conclusions parsed from the report. Use this to obtain
    the patient's pharmacogenomic profile (CYP2D6, CYP2C19, CYP2C9, VKORC1, DPYD)
    before running the pharmacogenomic_medication_review skill.
    """
    ctx = _get_fhir_context(tool_context)
    if isinstance(ctx, dict):
        return ctx
    fhir_url, fhir_token, patient_id = ctx

    logger.info("tool_get_pgx_panel patient_id=%s", patient_id)
    try:
        bundle = _fhir_get(
            fhir_url, fhir_token, "DiagnosticReport",
            params={"patient": patient_id, "category": "GE", "_count": "10", "_sort": "-date"},
        )
        # Some servers ignore the category filter — fall back to all reports
        if not bundle.get("entry"):
            bundle = _fhir_get(
                fhir_url, fhir_token, "DiagnosticReport",
                params={"patient": patient_id, "_count": "20", "_sort": "-date"},
            )
    except httpx.HTTPStatusError as e:
        return _http_error_result(e)
    except Exception as e:
        return _connection_error_result(e)

    reports = []
    for entry in bundle.get("entry", []):
        res = entry.get("resource", {})
        code = res.get("code", {})
        title = code.get("text") or _coding_display(code.get("coding", []))
        # Only surface PGx-flavoured reports
        is_pgx = any(
            kw in (title or "").lower()
            for kw in ("pharmacogenomic", "pgx", "pharmacogenetic", "drug-gene", "genomic")
        )
        if not is_pgx:
            continue
        reports.append({
            "report_id":      res.get("id"),
            "title":          title,
            "effective_date": res.get("effectiveDateTime")
                              or (res.get("effectivePeriod") or {}).get("start"),
            "conclusion":     res.get("conclusion"),
            "status":         res.get("status"),
        })

    # Parse the most recent report's conclusion into structured diplotypes (free-text format).
    parsed_variants: list[str] = []
    if reports:
        import re
        conclusion = reports[0].get("conclusion") or ""
        # Match patterns like "CYP2D6 *4/*4", "VKORC1 -1639 GG", "DPYD wild-type"
        for m in re.finditer(
            r"(CYP2D6|CYP2C19|CYP2C9|CYP3A4|VKORC1|DPYD|UGT1A1|TPMT|SLCO1B1)"
            r"\s*(?:-?\d+\s*[A-Z]?>?[A-Z]?\s*)?"
            r"(\*\w+\s*/\s*\*\w+|\*\w+|AA|AG|GG|GA|wild-type)",
            conclusion,
            re.IGNORECASE,
        ):
            gene = m.group(1).upper()
            allele = m.group(2).strip()
            parsed_variants.append(f"{gene} {allele}")

    return {
        "status":          "success",
        "patient_id":      patient_id,
        "count":           len(reports),
        "reports":         reports,
        "parsed_variants": parsed_variants,
        "variants_string": ", ".join(parsed_variants),
    }
