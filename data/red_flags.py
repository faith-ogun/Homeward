"""
Red-flag symptom rules for post-surgical recovery monitoring.

Defines universal red flags (all procedures) and provides functions to
check patient-reported symptoms against these rules. Procedure-specific
red flags are defined in data/procedures.py.

All thresholds are deterministic — NOT LLM-generated.
"""

# ── Universal Red Flags (apply to ALL procedures) ─────────────────────────────

UNIVERSAL_RED_FLAGS: list[dict] = [
    {
        "id": "fever",
        "symptom": "Fever",
        "threshold": "Temperature >38.0°C (100.4°F)",
        "threshold_value": 38.0,  # Celsius
        "severity": "RED",
        "clinical_concern": "Possible surgical site infection, UTI, pneumonia, or other post-operative infection",
        "action": "Contact surgical team immediately. May require blood cultures, wound assessment, and empiric antibiotics.",
    },
    {
        "id": "pain_increasing",
        "symptom": "Increasing pain after initial improvement",
        "threshold": "Pain increasing by >=2 points after day 3, or any sudden severe pain",
        "severity": "RED",
        "clinical_concern": "Possible surgical complication: infection, haematoma, anastomotic leak, compartment syndrome",
        "action": "Urgent clinical review. May require imaging and examination.",
    },
    {
        "id": "wound_purulent",
        "symptom": "Purulent wound drainage",
        "threshold": "Foul-smelling, cloudy, or pus-like drainage from incision",
        "severity": "RED",
        "clinical_concern": "Surgical site infection (SSI)",
        "action": "Contact surgical team. Wound culture, possible antibiotics, possible wound exploration.",
    },
    {
        "id": "wound_spreading_redness",
        "symptom": "Spreading redness beyond incision margins",
        "threshold": "Redness extending >2cm from incision edge, or redness increasing in area",
        "severity": "AMBER",
        "clinical_concern": "Possible cellulitis or superficial SSI",
        "action": "Clinical review within 24 hours. Monitor closely. May need antibiotics.",
    },
    {
        "id": "dvt_signs",
        "symptom": "DVT signs (calf)",
        "threshold": "Unilateral calf swelling, warmth, tenderness, or pain with dorsiflexion",
        "severity": "RED",
        "clinical_concern": "Deep vein thrombosis — risk of pulmonary embolism",
        "action": "Urgent clinical review. Duplex ultrasound of lower extremities. Do not massage affected leg.",
    },
    {
        "id": "pe_signs",
        "symptom": "PE signs (chest/breathing)",
        "threshold": "Chest pain, sudden shortness of breath, tachycardia, or haemoptysis",
        "severity": "RED",
        "clinical_concern": "Pulmonary embolism — life-threatening emergency",
        "action": "Call emergency services (999/911). Do not delay. CT pulmonary angiogram required.",
    },
    {
        "id": "oral_intake_failure",
        "symptom": "Unable to keep down fluids",
        "threshold": "Persistent nausea/vomiting preventing oral intake for >24 hours",
        "severity": "AMBER",
        "clinical_concern": "Dehydration, medication non-compliance, possible ileus or obstruction",
        "action": "Clinical review. May need IV fluids, antiemetics, and assessment for ileus.",
    },
    {
        "id": "wound_dehiscence",
        "symptom": "Wound opening",
        "threshold": "Incision edges separating, visible subcutaneous tissue or deeper structures",
        "severity": "RED",
        "clinical_concern": "Wound dehiscence — risk of infection and evisceration (abdominal surgery)",
        "action": "Cover with clean, moist dressing. Contact surgical team immediately.",
    },
]


# ── Symptom checking functions ─────────────────────────────────────────────────

def check_temperature(temperature_celsius: float) -> dict | None:
    """
    Check if a temperature reading triggers a red flag.
    Returns the flag dict if triggered, None if normal.
    """
    if temperature_celsius >= 38.0:
        return {
            "flag": "fever",
            "severity": "RED",
            "reported_value": f"{temperature_celsius}°C",
            "threshold": ">38.0°C (100.4°F)",
            "concern": "Possible post-operative infection",
            "action": "Contact surgical team immediately",
        }
    elif temperature_celsius >= 37.5:
        return {
            "flag": "low_grade_fever",
            "severity": "WATCH",
            "reported_value": f"{temperature_celsius}°C",
            "threshold": "37.5-37.9°C — low-grade, monitor",
            "concern": "Low-grade temperature elevation. Common in first 48 hours post-op. Watch for trend.",
            "action": "Monitor temperature every 4-6 hours. If rising or >38°C, contact surgical team.",
        }
    return None


def check_pain_trajectory(
    current_pain: int,
    post_op_day: int,
    expected_range: tuple[int, int],
    previous_pain: int | None = None,
) -> dict:
    """
    Assess pain level against expected range and trajectory.

    Args:
        current_pain: Current pain level (0-10)
        post_op_day: Days since surgery
        expected_range: (min, max) expected pain for this day/procedure
        previous_pain: Previous reported pain level (if available)

    Returns assessment dict with status and reasoning.
    """
    min_expected, max_expected = expected_range

    # Check if pain is above expected range
    if current_pain > max_expected:
        severity = "RED" if current_pain >= max_expected + 3 else "AMBER"
        status = "ABOVE_EXPECTED"
        reasoning = (
            f"Pain {current_pain}/10 exceeds expected range of {min_expected}-{max_expected} "
            f"for post-op day {post_op_day}."
        )
    elif current_pain < min_expected:
        status = "BELOW_EXPECTED"
        severity = "GREEN"
        reasoning = f"Pain {current_pain}/10 is below expected range. Good progress."
    else:
        status = "WITHIN_EXPECTED"
        severity = "GREEN"
        reasoning = f"Pain {current_pain}/10 is within expected range of {min_expected}-{max_expected}."

    # Check trajectory if previous pain is available
    if previous_pain is not None and post_op_day > 3:
        if current_pain > previous_pain + 1:
            severity = "RED" if severity != "RED" else severity
            status = "INCREASING"
            reasoning += (
                f" Pain has increased from {previous_pain} to {current_pain} — "
                "pain should be declining at this stage. Possible complication."
            )

    return {
        "pain_level": current_pain,
        "expected_range": list(expected_range),
        "status": status,
        "severity": severity,
        "reasoning": reasoning,
    }


def check_wound_description(description: str) -> dict:
    """
    Analyse a wound description for red-flag keywords.
    Returns assessment with severity level.
    """
    desc_lower = description.lower()

    red_keywords = [
        ("purulent", "Purulent drainage suggests infection"),
        ("pus", "Pus indicates possible surgical site infection"),
        ("foul", "Foul-smelling drainage suggests infection"),
        ("opening", "Wound opening suggests dehiscence"),
        ("dehiscence", "Wound dehiscence requires urgent review"),
        ("gaping", "Wound gaping suggests dehiscence"),
        ("spreading redness", "Spreading redness suggests cellulitis"),
    ]

    amber_keywords = [
        ("redness", "Redness around incision — monitor for spreading"),
        ("red", "Redness noted — monitor for worsening"),
        ("swelling", "Swelling beyond expected — monitor closely"),
        ("swollen", "Swelling noted — monitor for worsening"),
        ("warm", "Warmth around incision may indicate early infection"),
        ("drainage", "Drainage present — monitor colour and amount"),
        ("oozing", "Oozing from incision — monitor for increase"),
        ("bleeding", "Bleeding from incision — monitor amount"),
    ]

    green_keywords = [
        ("healing", "Wound healing as expected"),
        ("clean", "Clean wound — good progress"),
        ("dry", "Dry incision — normal healing"),
        ("normal", "Wound appears normal"),
        ("good", "Wound looks good"),
    ]

    # Check for red flags first
    for keyword, concern in red_keywords:
        if keyword in desc_lower:
            return {
                "status": "RED",
                "description": description,
                "finding": concern,
                "action": "Contact surgical team immediately for wound assessment.",
            }

    # Then amber
    for keyword, concern in amber_keywords:
        if keyword in desc_lower:
            return {
                "status": "AMBER",
                "description": description,
                "finding": concern,
                "action": "Monitor closely. If worsening within 24 hours, contact surgical team.",
            }

    # Then green
    for keyword, concern in green_keywords:
        if keyword in desc_lower:
            return {
                "status": "GREEN",
                "description": description,
                "finding": concern,
                "action": "Continue standard wound care.",
            }

    # Default — can't determine from description
    return {
        "status": "WATCH",
        "description": description,
        "finding": "Wound status could not be fully assessed from description alone.",
        "action": "If concerned, take a photo and share with surgical team at next follow-up.",
    }


def check_symptoms_for_red_flags(symptoms: str) -> list[dict]:
    """
    Check a free-text symptom description against universal red flag patterns.
    Returns a list of triggered flags (may be empty).
    """
    symp_lower = symptoms.lower()
    triggered = []

    symptom_patterns = {
        "dvt_signs": ["calf pain", "calf swelling", "leg swelling", "calf tender", "leg pain and swelling"],
        "pe_signs": ["chest pain", "shortness of breath", "difficulty breathing", "coughing blood", "rapid heart"],
        "wound_dehiscence": ["wound open", "incision open", "wound coming apart", "stitches broke"],
        "wound_purulent": ["pus", "purulent", "foul smell", "green discharge", "yellow discharge"],
        "oral_intake_failure": ["can't keep food down", "vomiting all day", "can't eat", "can't drink"],
    }

    for flag_id, patterns in symptom_patterns.items():
        for pattern in patterns:
            if pattern in symp_lower:
                # Find the matching universal flag
                for flag in UNIVERSAL_RED_FLAGS:
                    if flag["id"] == flag_id:
                        triggered.append({
                            "flag_id": flag_id,
                            "matched_pattern": pattern,
                            "severity": flag["severity"],
                            "clinical_concern": flag["clinical_concern"],
                            "action": flag["action"],
                        })
                        break
                break  # Only trigger each flag once

    return triggered


def get_overall_severity(*severities: str) -> str:
    """
    Determine the highest severity level from multiple assessments.
    RED > AMBER > WATCH > GREEN
    """
    priority = {"RED": 4, "AMBER": 3, "WATCH": 2, "GREEN": 1}
    max_severity = "GREEN"
    max_priority = 0

    for s in severities:
        p = priority.get(s.upper(), 0)
        if p > max_priority:
            max_priority = p
            max_severity = s.upper()

    return max_severity
