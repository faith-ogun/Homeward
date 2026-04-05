"""
Skill 4: Escalation Summary Generator

Generates structured GREEN/AMBER/RED clinical summary combining recovery
assessment, pharmacogenomic flags, and recommended actions.
"""
import logging

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


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
        escalation_level: The escalation classification — must be one of
            'GREEN' (on track), 'AMBER' (watch/review needed), or 'RED' (escalate immediately).
        recovery_summary: Summary of the recovery assessment findings
            (e.g. 'Pain 7/10 on day 4, above expected range of 2-5').
        pgx_summary: Summary of pharmacogenomic findings
            (e.g. 'CYP2D6 poor metabolizer on codeine — drug likely ineffective')
            or 'No pharmacogenomic flags' if none.
        recommended_actions: Comma-separated list of recommended clinical actions
            (e.g. 'Switch analgesic, Monitor wound redness, Follow up in 24 hours').

    Returns a structured clinical summary with care team guidance and patient-facing messaging.
    """
    patient_id = tool_context.state.get("patient_id", "unknown")
    logger.info(
        "tool_generate_escalation_summary patient_id=%s level=%s",
        patient_id, escalation_level,
    )

    actions_list = [a.strip() for a in recommended_actions.split(",") if a.strip()]

    return {
        "status": "success",
        "patient_id": patient_id,
        "escalation_level": escalation_level.upper(),
        "summary": (
            f"Escalation level: {escalation_level.upper()}. "
            f"Recovery: {recovery_summary}. "
            f"Pharmacogenomics: {pgx_summary}."
        ),
        "recommended_actions": actions_list,
        "for_care_team": (
            f"Recovery assessment: {recovery_summary}. "
            f"PGx findings: {pgx_summary}. "
            "Please review the recommended actions and determine appropriate next steps."
        ),
        "patient_guidance": (
            "Your care team has been notified about your recovery progress. "
            "They will review your status and may reach out with updated guidance. "
            "If you experience any emergency symptoms (severe pain, difficulty breathing, "
            "high fever), contact emergency services immediately."
        ),
        "not_an_emergency": escalation_level.upper() != "RED",
        "note": "This is a stub response. Full implementation will use LLM to generate contextualised summaries.",
    }
