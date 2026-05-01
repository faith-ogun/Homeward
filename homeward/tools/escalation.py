"""
Skill 4: Escalation Summary Generator

Combines recovery assessment, PGx flags, and clinical reasoning into a
structured GREEN/AMBER/RED summary with separate care-team and patient-facing
messaging. Deterministic severity rules and templates; the LLM provides the
synthesis text.
"""
import logging

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


# ── Severity templates ────────────────────────────────────────────────────────

_SEVERITY_TEMPLATES = {
    "GREEN": {
        "headline": "On track — no immediate action required",
        "urgency": "Routine — no clinician contact needed",
        "default_actions": [
            "Continue current recovery plan as prescribed",
            "Maintain scheduled follow-up appointment",
            "Patient should report any new or worsening symptoms",
        ],
        "patient_default": (
            "Your recovery is tracking as expected. Continue following your discharge "
            "instructions. If you develop any new or concerning symptoms, contact your "
            "care team."
        ),
    },
    "AMBER": {
        "headline": "Recovery deviation — clinician review recommended",
        "urgency": "Within 24 hours — non-emergency clinical review",
        "default_actions": [
            "Schedule clinician review within 24 hours",
            "Monitor flagged symptoms and document any progression",
            "Reassess if symptoms worsen — escalate to RED",
        ],
        "patient_default": (
            "Your recovery shows some signs that warrant a closer look. This is not an "
            "emergency. We recommend contacting your care team to discuss next steps. If "
            "your symptoms get worse before you reach them, seek urgent medical attention."
        ),
    },
    "RED": {
        "headline": "Escalation required — urgent clinical attention",
        "urgency": "Immediate — surgical team or emergency services",
        "default_actions": [
            "Contact surgical team immediately",
            "Consider in-person assessment / emergency department evaluation",
            "Do not delay — possible complication requiring intervention",
        ],
        "patient_default": (
            "Your symptoms suggest a possible complication that needs urgent attention. "
            "Please contact your surgical team immediately or go to your nearest emergency "
            "department. Do not wait."
        ),
    },
}


def _normalise_level(level: str) -> str:
    if not level:
        return "AMBER"
    upper = level.strip().upper()
    if upper in ("GREEN", "AMBER", "RED"):
        return upper
    # Map related terms
    if upper in ("ON_TRACK", "OK", "NORMAL", "CLEAR"):
        return "GREEN"
    if upper in ("WATCH", "MONITOR", "CAUTION"):
        return "AMBER"
    if upper in ("ESCALATE", "URGENT", "EMERGENCY"):
        return "RED"
    return "AMBER"


def generate_escalation_summary(
    escalation_level: str,
    recovery_summary: str,
    pgx_summary: str,
    recommended_actions: str,
    tool_context: ToolContext,
) -> dict:
    """
    Generates a structured escalation summary for the care team and patient.

    Args:
        escalation_level: 'GREEN' (on track), 'AMBER' (watch/review), or 'RED' (escalate).
        recovery_summary: Findings from the recovery assessment
            (e.g. 'Pain 7/10 on day 4, above expected range of 2-5; slight wound redness').
        pgx_summary: Summary of pharmacogenomic findings
            (e.g. 'CYP2D6 poor metabolizer on codeine — drug likely ineffective')
            or 'No pharmacogenomic flags' if none.
        recommended_actions: Comma-separated clinical actions
            (e.g. 'Switch analgesic, Monitor wound, Follow up in 24h').

    Returns a structured clinical summary with care-team and patient guidance.
    """
    patient_id = tool_context.state.get("patient_id", "unknown")
    level = _normalise_level(escalation_level)
    logger.info(
        "tool_generate_escalation_summary patient_id=%s level=%s",
        patient_id, level,
    )

    template = _SEVERITY_TEMPLATES[level]

    actions_list = [a.strip() for a in (recommended_actions or "").split(",") if a.strip()]
    if not actions_list:
        actions_list = list(template["default_actions"])

    procedure = tool_context.state.get("procedure", "post-surgical recovery")
    post_op_day = tool_context.state.get("post_op_day")
    day_str = f"day {post_op_day} " if post_op_day else ""

    care_team_summary = (
        f"[{level}] {template['headline']}. "
        f"Patient {patient_id}, {day_str}post-{procedure}. "
        f"Recovery findings: {recovery_summary}. "
        f"Pharmacogenomics: {pgx_summary}. "
        f"Urgency: {template['urgency']}."
    )

    return {
        "status": "success",
        "patient_id": patient_id,
        "escalation_level": level,
        "headline": template["headline"],
        "urgency": template["urgency"],
        "is_emergency": level == "RED",
        "not_an_emergency": level != "RED",
        "for_care_team": care_team_summary,
        "recovery_summary": recovery_summary,
        "pgx_summary": pgx_summary,
        "recommended_actions": actions_list,
        "patient_guidance": template["patient_default"],
        "structured_summary": {
            "level": level,
            "headline": template["headline"],
            "patient_id": patient_id,
            "procedure": procedure,
            "post_op_day": post_op_day,
            "recovery": recovery_summary,
            "pgx": pgx_summary,
            "actions": actions_list,
            "urgency": template["urgency"],
        },
    }
