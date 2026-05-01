"""
Skill 1: Discharge Note Interpreter

Returns the canonical, evidence-based recovery timeline for a given procedure
and computes which phase the patient is currently in based on their surgery date.

The deterministic procedure data comes from data/procedures.py. The LLM caller
combines this structured timeline with the free-text discharge_text it was
given to produce a fully personalised summary (medications, schedules,
patient-specific restrictions extracted from the note itself).
"""
import logging
from datetime import date, datetime

from google.adk.tools import ToolContext

from data.procedures import find_procedure, get_timeline_phase, list_procedure_names

logger = logging.getLogger(__name__)


def _parse_date(date_str: str) -> date | None:
    """Parse YYYY-MM-DD or DD/MM/YYYY. Return None if unparseable."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None


def interpret_discharge_note(
    procedure_name: str,
    surgery_date: str,
    discharge_text: str,
    tool_context: ToolContext,
) -> dict:
    """
    Returns the structured recovery timeline for a procedure plus the patient's
    current post-op phase based on the surgery date.

    Args:
        procedure_name: Surgical procedure name or alias
            (e.g. 'Robotic Prostatectomy', 'lap chole', 'TKR').
        surgery_date: Date of surgery in YYYY-MM-DD format.
        discharge_text: Full text of the discharge instructions document.
            (Returned to the caller for cross-reference; the LLM extracts
            medication schedules and patient-specific instructions from it.)

    Returns structured timeline, current phase, red flags, and discharge text excerpt.
    """
    patient_id = tool_context.state.get("patient_id", "unknown")
    logger.info(
        "tool_interpret_discharge_note patient_id=%s procedure=%s surgery_date=%s text_len=%d",
        patient_id, procedure_name, surgery_date, len(discharge_text or ""),
    )

    proc = find_procedure(procedure_name)
    if not proc:
        return {
            "status": "procedure_not_found",
            "patient_id": patient_id,
            "requested_procedure": procedure_name,
            "supported_procedures": list_procedure_names(),
            "message": (
                f"Procedure '{procedure_name}' is not in the supported list. "
                f"Recovery timeline cannot be retrieved without a recognised procedure."
            ),
        }

    surgery_dt = _parse_date(surgery_date)
    today = date.today()

    if surgery_dt:
        post_op_day = (today - surgery_dt).days
    else:
        post_op_day = None

    current_phase = None
    if post_op_day is not None and post_op_day >= 0:
        current_phase = get_timeline_phase(proc["display_name"], post_op_day)

    return {
        "status": "success",
        "patient_id": patient_id,
        "procedure": proc["display_name"],
        "surgery_date": surgery_date,
        "today": today.isoformat(),
        "post_op_day": post_op_day,
        "typical_recovery_days": proc["typical_recovery_days"],
        "typical_hospital_stay_days": proc["typical_hospital_stay_days"],
        "typical_medications": proc["typical_medications"],
        "current_phase": current_phase,
        "full_recovery_timeline": proc["timeline"],
        "red_flags": proc["red_flags"],
        "discharge_text_excerpt": (discharge_text or "")[:2000],
        "discharge_text_length": len(discharge_text or ""),
        "guidance_for_caller": (
            "Use the discharge_text_excerpt to extract patient-specific medication "
            "schedules, dose instructions, follow-up dates, and any restrictions that "
            "are unique to this patient. Combine with the deterministic full_recovery_timeline "
            "and red_flags above for the personalised summary."
        ),
    }
