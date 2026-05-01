"""
Skill 3: Recovery Check-In Assessment

Compares patient-reported symptoms against the procedure-specific expected
recovery timeline and applies deterministic red-flag rules. The PGx context
(if any flags exist) is integrated to distinguish surgical complications from
medication inefficacy.
"""
import logging

from google.adk.tools import ToolContext

from data.procedures import get_timeline_phase, find_procedure
from data.red_flags import (
    check_pain_trajectory,
    check_symptoms_for_red_flags,
    check_temperature,
    check_wound_description,
    get_overall_severity,
)

logger = logging.getLogger(__name__)


def assess_recovery_checkin(
    procedure_name: str,
    post_op_day: int,
    pain_level: int,
    temperature: float,
    wound_description: str,
    mobility_description: str,
    other_symptoms: str,
    tool_context: ToolContext,
) -> dict:
    """
    Assesses a patient's recovery check-in against expected recovery trajectory.

    Args:
        procedure_name: The surgical procedure performed (e.g. 'Robotic Prostatectomy').
        post_op_day: Number of days since surgery (e.g. 4).
        pain_level: Patient-reported pain level on a 0-10 scale.
        temperature: Patient's temperature in Celsius (e.g. 37.2).
        wound_description: Patient's description of wound appearance.
        mobility_description: Patient's description of current mobility.
        other_symptoms: Any additional symptoms reported (or 'None').

    Returns assessment with on-track/watch/escalate classification, red-flag
    findings, PGx context if available, and clinical reasoning.
    """
    patient_id = tool_context.state.get("patient_id", "unknown")
    logger.info(
        "tool_assess_recovery_checkin patient_id=%s procedure=%s day=%d pain=%d temp=%.1f",
        patient_id, procedure_name, post_op_day, pain_level, temperature,
    )

    proc = find_procedure(procedure_name)
    if not proc:
        return {
            "status": "procedure_not_found",
            "patient_id": patient_id,
            "requested_procedure": procedure_name,
            "message": (
                f"Procedure '{procedure_name}' is not in the supported list. "
                f"Cannot assess recovery without a recognised expected timeline."
            ),
        }

    phase = get_timeline_phase(proc["display_name"], post_op_day)

    # ── Pain assessment ───────────────────────────────────────────────────────
    if phase:
        expected_range = tuple(phase["expected_pain_range"])
        previous_pain = tool_context.state.get("previous_pain_level")
        pain_assessment = check_pain_trajectory(
            current_pain=pain_level,
            post_op_day=post_op_day,
            expected_range=expected_range,
            previous_pain=previous_pain,
        )
    else:
        pain_assessment = {
            "pain_level": pain_level,
            "expected_range": None,
            "status": "OUT_OF_TIMELINE",
            "severity": "WATCH",
            "reasoning": f"Day {post_op_day} is outside the standard recovery timeline window for this procedure.",
        }

    # ── Temperature assessment ────────────────────────────────────────────────
    temp_flag = check_temperature(temperature)
    temp_severity = temp_flag["severity"] if temp_flag else "GREEN"
    temp_assessment = {
        "reported": temperature,
        "severity": temp_severity,
        "finding": temp_flag if temp_flag else {
            "flag": "normal",
            "severity": "GREEN",
            "reported_value": f"{temperature}°C",
            "concern": "Temperature within normal range.",
        },
    }

    # ── Wound assessment ──────────────────────────────────────────────────────
    wound_assessment = check_wound_description(wound_description or "")

    # ── Mobility (heuristic) ──────────────────────────────────────────────────
    mob_lower = (mobility_description or "").lower()
    if any(k in mob_lower for k in ["bedbound", "cannot walk", "unable to walk", "not walking"]):
        mobility_severity = "AMBER"
        mobility_finding = "Reduced mobility — increased DVT/PE and pneumonia risk. Encourage walking as tolerated."
    elif any(k in mob_lower for k in ["walking", "ambulating", "moving", "active"]):
        mobility_severity = "GREEN"
        mobility_finding = "Mobility tracking as expected for recovery phase."
    else:
        mobility_severity = "WATCH"
        mobility_finding = "Mobility status unclear from report — clarify at next check-in."

    mobility_assessment = {
        "reported": mobility_description,
        "severity": mobility_severity,
        "finding": mobility_finding,
    }

    # ── Other symptoms — universal red flag pattern matching ──────────────────
    symptom_flags = check_symptoms_for_red_flags(other_symptoms or "")

    # ── PGx context integration ───────────────────────────────────────────────
    # Skill 2 output (if previously called in this session) is in tool_context.state.
    pgx_context: dict | str | None = None
    pgx_flags = tool_context.state.get("last_pgx_flags") or []
    if pgx_flags:
        pain_status = pain_assessment.get("status")
        relevant_pgx = [
            f for f in pgx_flags
            if f.get("gene") in ("CYP2D6", "CYP2C19", "CYP2C9")
            and f.get("risk_level") in ("HIGH", "MODERATE")
        ]
        if pain_status in ("ABOVE_EXPECTED", "INCREASING") and relevant_pgx:
            pgx_context = {
                "interpretation": (
                    "Patient has actionable PGx flags. Elevated pain may reflect medication "
                    "inefficacy (drug-gene interaction) rather than a surgical complication. "
                    "Review analgesic before assuming complication."
                ),
                "relevant_flags": relevant_pgx,
            }
        else:
            pgx_context = {
                "interpretation": "PGx flags exist but do not directly explain the current symptom profile.",
                "relevant_flags": pgx_flags,
            }
    else:
        pgx_context = (
            "No PGx review performed yet for this patient in this session. "
            "Consider running pharmacogenomic_medication_review if patient has uncontrolled "
            "pain or unusual medication response."
        )

    # ── Overall severity ──────────────────────────────────────────────────────
    severities = [
        pain_assessment.get("severity", "GREEN"),
        temp_severity,
        wound_assessment.get("status", "GREEN"),
        mobility_severity,
    ]
    for f in symptom_flags:
        severities.append(f.get("severity", "GREEN"))

    overall_severity = get_overall_severity(*severities)
    status_map = {"RED": "ESCALATE", "AMBER": "WATCH", "WATCH": "WATCH", "GREEN": "ON_TRACK"}
    overall_status = status_map.get(overall_severity, "WATCH")

    return {
        "status": "success",
        "patient_id": patient_id,
        "procedure": proc["display_name"],
        "post_op_day": post_op_day,
        "current_phase": phase["phase"] if phase else None,
        "expected_for_this_phase": {
            "pain_range": phase["expected_pain_range"] if phase else None,
            "pain_trend": phase["expected_pain_trend"] if phase else None,
            "mobility": phase["mobility"] if phase else None,
            "wound_status": phase["wound_status"] if phase else None,
        } if phase else None,
        "assessment": {
            "pain": pain_assessment,
            "temperature": temp_assessment,
            "wound": wound_assessment,
            "mobility": mobility_assessment,
            "other_symptoms": {
                "reported": other_symptoms,
                "red_flag_matches": symptom_flags,
            },
        },
        "pgx_context": pgx_context,
        "overall_severity": overall_severity,
        "overall_status": overall_status,
        "summary": (
            f"Day {post_op_day} post-{proc['display_name']}. "
            f"Pain {pain_level}/10 ({pain_assessment.get('status', 'unknown')}). "
            f"Temp {temperature}°C ({temp_severity}). "
            f"Wound: {wound_assessment.get('status', 'unknown')}. "
            f"Overall: {overall_severity}."
        ),
    }
