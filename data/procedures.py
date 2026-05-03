"""
Procedure-specific recovery timelines and milestones.

All data is deterministic — sourced from published surgical recovery literature,
NOT LLM-generated. Each procedure defines expected pain trajectories, mobility
milestones, wound healing stages, typical medications, and red-flag symptoms
by post-operative day.

Pain ranges are on a 0-10 numeric scale (patient self-report).
Temperature thresholds are in Celsius.
"""

# ── Data structures ────────────────────────────────────────────────────────────

# Each timeline phase has:
#   days: (start_day, end_day) inclusive
#   expected_pain_range: [min, max] on 0-10 scale
#   expected_pain_trend: description of expected trajectory
#   mobility: expected mobility level
#   wound_status: expected wound appearance
#   key_instructions: list of care instructions for this phase

PROCEDURES: dict[str, dict] = {

    # ── 1. Robotic Prostatectomy (da Vinci) ──────────────────────────────────

    "robotic_prostatectomy": {
        "display_name": "Robotic Prostatectomy",
        "aliases": [
            "robotic prostatectomy", "da vinci prostatectomy",
            "robot-assisted prostatectomy", "RALP", "radical prostatectomy",
        ],
        "typical_recovery_days": 42,
        "typical_hospital_stay_days": 1,
        "typical_medications": ["Codeine", "Oxycodone", "Acetaminophen", "Enoxaparin", "Ondansetron", "Docusate"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [4, 7],
                "expected_pain_trend": "Moderate pain, should begin declining by day 2-3",
                "mobility": "Short walks around the house, avoid stairs if possible",
                "wound_status": "Port-site incisions may have mild bruising, slight swelling; steri-strips intact",
                "key_instructions": [
                    "Catheter care — keep drainage bag below bladder level",
                    "Ice application 20 minutes on / 20 minutes off to lower abdomen",
                    "No heavy lifting (>10 lbs / 4.5 kg)",
                    "Stool softener to avoid straining",
                    "Deep breathing exercises to prevent atelectasis",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [2, 5],
                "expected_pain_trend": "Declining; should be manageable with oral pain medication",
                "mobility": "Gradual increase in walking distance, light household activity",
                "wound_status": "Bruising fading, incisions drying, minimal drainage",
                "key_instructions": [
                    "Transition from opioid to non-opioid pain management if tolerated",
                    "Continue anticoagulation as prescribed",
                    "Begin pelvic floor exercises (Kegels) if cleared",
                    "No driving while on opioid pain medication",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [1, 3],
                "expected_pain_trend": "Minimal discomfort, mostly positional",
                "mobility": "Normal walking, no heavy lifting >10 lbs, no strenuous exercise",
                "wound_status": "Incisions healing well, steri-strips may begin to fall off",
                "key_instructions": [
                    "Catheter removal typically day 7-14 (per surgeon instruction)",
                    "Follow-up appointment with urology",
                    "Resume light work if non-physical",
                    "Continue pelvic floor exercises",
                ],
            },
            {
                "phase": "days_15_42",
                "days": (15, 42),
                "expected_pain_range": [0, 2],
                "expected_pain_trend": "Rare mild discomfort only",
                "mobility": "Gradual return to full activity; avoid heavy lifting until 6 weeks",
                "wound_status": "Fully healed incisions",
                "key_instructions": [
                    "Gradual return to exercise at 4-6 weeks",
                    "Continue pelvic floor rehabilitation",
                    "PSA testing as scheduled by oncologist",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Increasing pain after initial improvement (day 3+)",
            "Wound redness, swelling, warmth, or purulent drainage",
            "Inability to urinate after catheter removal",
            "Blood clots in urine (large or increasing)",
            "Swelling, warmth, or tenderness in calf or leg (DVT signs)",
            "Chest pain or sudden shortness of breath (PE signs)",
            "Persistent nausea/vomiting preventing oral intake >24 hours",
        ],
    },

    # ── 2. Laparoscopic Cholecystectomy ──────────────────────────────────────

    "laparoscopic_cholecystectomy": {
        "display_name": "Laparoscopic Cholecystectomy",
        "aliases": [
            "laparoscopic cholecystectomy", "lap chole", "gallbladder removal",
            "cholecystectomy", "laparoscopic gallbladder",
        ],
        "typical_recovery_days": 14,
        "typical_hospital_stay_days": 0,  # same-day discharge typical
        "typical_medications": ["Acetaminophen", "Ibuprofen", "Oxycodone", "Ondansetron"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [3, 6],
                "expected_pain_trend": "Moderate incisional and referred shoulder pain (CO2), declining",
                "mobility": "Walking same day, short distances; avoid heavy activity",
                "wound_status": "4 small port-site incisions, mild bruising, steri-strips",
                "key_instructions": [
                    "Shoulder pain from CO2 insufflation is normal — will resolve in 24-72 hours",
                    "Low-fat diet for 1-2 weeks to reduce GI symptoms",
                    "Alternate acetaminophen and ibuprofen for pain",
                    "Use opioids only for breakthrough pain",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [1, 3],
                "expected_pain_trend": "Mild discomfort, mostly around incision sites",
                "mobility": "Normal walking, light activity; avoid lifting >15 lbs",
                "wound_status": "Incisions drying, bruising fading",
                "key_instructions": [
                    "Return to light work/desk job if comfortable",
                    "Gradual reintroduction of regular diet",
                    "Discontinue opioids if not needed",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [0, 1],
                "expected_pain_trend": "Minimal to no pain",
                "mobility": "Return to most normal activities; no heavy lifting until 2 weeks",
                "wound_status": "Well-healed port sites",
                "key_instructions": [
                    "Follow-up appointment if scheduled",
                    "Resume exercise gradually",
                    "Normal diet tolerated",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Worsening abdominal pain (especially right upper quadrant)",
            "Jaundice (yellowing of skin or eyes)",
            "Persistent nausea/vomiting >24 hours",
            "Wound redness, swelling, or purulent drainage",
            "Dark urine or clay-coloured stools (bile duct issue)",
            "Chest pain or shortness of breath",
        ],
    },

    # ── 3. Total Knee Replacement (robotic-assisted) ─────────────────────────

    "total_knee_replacement": {
        "display_name": "Total Knee Replacement",
        "aliases": [
            "total knee replacement", "TKR", "total knee arthroplasty", "TKA",
            "robotic knee replacement", "knee replacement",
        ],
        "typical_recovery_days": 84,  # 12 weeks
        "typical_hospital_stay_days": 1,
        "typical_medications": ["Oxycodone", "Acetaminophen", "Celecoxib", "Enoxaparin", "Cefazolin", "Ondansetron"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [5, 8],
                "expected_pain_trend": "Significant pain expected; managed with multimodal analgesia",
                "mobility": "Weight-bearing as tolerated with walker or crutches; physiotherapy begins day 1",
                "wound_status": "Surgical incision with staples/sutures, moderate swelling, possible drain",
                "key_instructions": [
                    "Ice and elevate knee 20 minutes on / 20 minutes off",
                    "Begin physiotherapy exercises immediately (quad sets, ankle pumps)",
                    "Use compression stockings and anticoagulation as prescribed",
                    "Continuous passive motion (CPM) machine if prescribed",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [4, 7],
                "expected_pain_trend": "Gradually improving; pain with movement is expected",
                "mobility": "Walking with assistive device, increasing distance daily; stairs with rail",
                "wound_status": "Swelling persists but should not be increasing; incision intact",
                "key_instructions": [
                    "Continue physiotherapy 2-3 times daily",
                    "Goal: 90 degrees knee flexion by end of week 1",
                    "Continue anticoagulation (typically 2-6 weeks)",
                    "Transition to oral-only pain management",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [3, 5],
                "expected_pain_trend": "Improving; worst pain during physiotherapy sessions",
                "mobility": "Walking longer distances; may begin reducing assistive device use",
                "wound_status": "Swelling slowly decreasing; staple/suture removal around day 10-14",
                "key_instructions": [
                    "Follow-up appointment for wound check and staple removal",
                    "Continue home physiotherapy program",
                    "May begin outpatient physiotherapy",
                    "Reduce opioid use — transition to non-opioid if possible",
                ],
            },
            {
                "phase": "days_15_84",
                "days": (15, 84),
                "expected_pain_range": [1, 4],
                "expected_pain_trend": "Steady improvement; exercise soreness is normal",
                "mobility": "Progressive return to function; full weight-bearing; driving at 4-6 weeks",
                "wound_status": "Healed incision; residual swelling may persist for months",
                "key_instructions": [
                    "Outpatient physiotherapy 2-3 times per week",
                    "Goal: 120 degrees flexion by 6 weeks",
                    "Return to light work at 4-6 weeks",
                    "Full recovery and maximum improvement at 3-6 months",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Increasing redness, warmth, or drainage from incision",
            "Sudden increase in knee swelling",
            "Calf pain, swelling, warmth, or tenderness (DVT signs)",
            "Chest pain, sudden shortness of breath (PE signs)",
            "Pain increasing rather than improving after day 5",
            "Inability to bear weight that was previously tolerated",
            "Numbness or tingling below the knee that is new or worsening",
        ],
    },

    # ── 4. Robotic Hysterectomy ──────────────────────────────────────────────

    "robotic_hysterectomy": {
        "display_name": "Robotic Hysterectomy",
        "aliases": [
            "robotic hysterectomy", "robot-assisted hysterectomy",
            "laparoscopic hysterectomy", "total hysterectomy", "hysterectomy",
        ],
        "typical_recovery_days": 42,
        "typical_hospital_stay_days": 1,
        "typical_medications": ["Acetaminophen", "Ibuprofen", "Oxycodone", "Ondansetron", "Enoxaparin", "Docusate"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [3, 6],
                "expected_pain_trend": "Moderate pelvic and incisional pain, declining",
                "mobility": "Walking same day; short distances, increasing gradually",
                "wound_status": "Small port-site incisions; mild bruising; vaginal cuff healing internally",
                "key_instructions": [
                    "No heavy lifting (>10 lbs / 4.5 kg)",
                    "Stool softener to prevent constipation and straining",
                    "Light vaginal bleeding or discharge is normal for 2-6 weeks",
                    "No vaginal intercourse, tampons, or douching for 6-8 weeks",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [2, 4],
                "expected_pain_trend": "Improving; mostly positional discomfort",
                "mobility": "Normal walking, light household tasks",
                "wound_status": "Incisions drying; some patients notice abdominal bloating",
                "key_instructions": [
                    "Transition to non-opioid pain management",
                    "Gradual increase in activity",
                    "Watch for signs of vaginal cuff dehiscence (sudden vaginal bleeding, pressure)",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [1, 2],
                "expected_pain_trend": "Minimal discomfort",
                "mobility": "Resume light work; no strenuous activity",
                "wound_status": "Port sites healed; bloating resolving",
                "key_instructions": [
                    "Follow-up appointment at 2 weeks",
                    "Continue activity restrictions (no heavy lifting, no vaginal insertion)",
                    "Return to desk work if comfortable",
                ],
            },
            {
                "phase": "days_15_42",
                "days": (15, 42),
                "expected_pain_range": [0, 1],
                "expected_pain_trend": "Rare discomfort only",
                "mobility": "Gradual return to full activity by 6 weeks",
                "wound_status": "Fully healed externally; vaginal cuff healing continues internally",
                "key_instructions": [
                    "Follow-up at 6 weeks — clearance for full activity and intercourse",
                    "Resume exercise gradually after 4 weeks",
                    "Report any new bleeding or unusual discharge",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Heavy vaginal bleeding (soaking a pad per hour)",
            "Foul-smelling vaginal discharge",
            "Sudden onset severe pelvic or abdominal pain",
            "Wound redness, swelling, or drainage",
            "Urinary retention or burning (UTI signs)",
            "Chest pain or shortness of breath (PE signs)",
            "Calf swelling, warmth, or tenderness (DVT signs)",
        ],
    },

    # ── 5. Laparoscopic Appendectomy ─────────────────────────────────────────

    "laparoscopic_appendectomy": {
        "display_name": "Laparoscopic Appendectomy",
        "aliases": [
            "laparoscopic appendectomy", "lap appy", "appendectomy",
            "appendix removal",
        ],
        "typical_recovery_days": 14,
        "typical_hospital_stay_days": 0,
        "typical_medications": ["Acetaminophen", "Ibuprofen", "Oxycodone", "Ondansetron"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [3, 6],
                "expected_pain_trend": "Moderate incisional pain, rapidly declining",
                "mobility": "Walking same day; short walks, avoid strenuous activity",
                "wound_status": "3 small port-site incisions; mild bruising",
                "key_instructions": [
                    "Alternate acetaminophen and ibuprofen",
                    "Use opioids only for breakthrough pain",
                    "Light diet progressing to normal as tolerated",
                    "Shoulder pain from CO2 is normal, resolves in 24-48 hours",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [1, 3],
                "expected_pain_trend": "Mild, improving daily",
                "mobility": "Normal walking; avoid heavy lifting >10 lbs",
                "wound_status": "Incisions drying, minimal tenderness",
                "key_instructions": [
                    "Return to school/desk work when comfortable",
                    "Normal diet",
                    "Discontinue opioids",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [0, 1],
                "expected_pain_trend": "Minimal to none",
                "mobility": "Full activity by 2 weeks; heavy lifting at 2-4 weeks",
                "wound_status": "Healed port sites",
                "key_instructions": [
                    "Follow-up only if complications arise",
                    "Resume sports and exercise at 2-4 weeks",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Increasing abdominal pain (especially right lower quadrant)",
            "Wound redness, swelling, or purulent drainage",
            "Persistent vomiting or inability to eat",
            "Abdominal distension or rigidity",
            "Chest pain or shortness of breath",
        ],
    },

    # ── 6. Robotic Partial Nephrectomy ───────────────────────────────────────

    "robotic_partial_nephrectomy": {
        "display_name": "Robotic Partial Nephrectomy",
        "aliases": [
            "robotic partial nephrectomy", "partial nephrectomy",
            "robot-assisted partial nephrectomy", "kidney tumour removal",
            "nephron-sparing surgery",
        ],
        "typical_recovery_days": 42,
        "typical_hospital_stay_days": 2,
        "typical_medications": ["Oxycodone", "Acetaminophen", "Enoxaparin", "Ondansetron", "Docusate"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [4, 7],
                "expected_pain_trend": "Moderate flank and incisional pain, declining",
                "mobility": "Walking in hospital; short walks at home",
                "wound_status": "Port-site incisions; possible drain site; mild bruising",
                "key_instructions": [
                    "Drain management if applicable",
                    "Maintain hydration — kidney function monitoring",
                    "No heavy lifting (>10 lbs / 4.5 kg)",
                    "Monitor urine output and colour",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [2, 5],
                "expected_pain_trend": "Improving; flank soreness may persist",
                "mobility": "Increasing walking; light household activity",
                "wound_status": "Drain removed if output decreasing; incisions drying",
                "key_instructions": [
                    "Continue hydration",
                    "Transition to non-opioid pain management",
                    "Follow-up blood work (creatinine, GFR) as ordered",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [1, 3],
                "expected_pain_trend": "Mild discomfort, mostly positional",
                "mobility": "Normal walking; avoid strenuous activity",
                "wound_status": "Incisions healing; drain site closed",
                "key_instructions": [
                    "Follow-up appointment — wound check and pathology results",
                    "Resume light work",
                    "Continue renal function monitoring",
                ],
            },
            {
                "phase": "days_15_42",
                "days": (15, 42),
                "expected_pain_range": [0, 2],
                "expected_pain_trend": "Minimal",
                "mobility": "Gradual return to full activity by 4-6 weeks",
                "wound_status": "Fully healed",
                "key_instructions": [
                    "Oncology follow-up and surveillance imaging schedule",
                    "Resume exercise at 4-6 weeks",
                    "Long-term renal function monitoring",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Flank pain that is suddenly worse or new",
            "Blood in urine (gross haematuria) after initial clearing",
            "Decreased urine output",
            "Wound redness, swelling, or drainage",
            "Persistent nausea/vomiting",
            "Chest pain or shortness of breath (PE signs)",
            "Calf swelling or tenderness (DVT signs)",
        ],
    },

    # ── 7. Laparoscopic Hernia Repair ────────────────────────────────────────

    "laparoscopic_hernia_repair": {
        "display_name": "Laparoscopic Hernia Repair",
        "aliases": [
            "laparoscopic hernia repair", "lap hernia", "inguinal hernia repair",
            "hernia repair", "TAPP", "TEP", "ventral hernia repair",
        ],
        "typical_recovery_days": 21,
        "typical_hospital_stay_days": 0,
        "typical_medications": ["Acetaminophen", "Ibuprofen", "Oxycodone", "Ondansetron"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [3, 6],
                "expected_pain_trend": "Moderate groin/abdominal pain, declining",
                "mobility": "Walking same day; avoid straining, bending, heavy lifting",
                "wound_status": "Small port-site incisions; groin swelling and bruising are common",
                "key_instructions": [
                    "Ice to groin area 20 minutes on / 20 minutes off",
                    "Wear supportive underwear or abdominal binder",
                    "Stool softener to avoid straining",
                    "Scrotal swelling (in inguinal repair) is normal and resolves in 1-2 weeks",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [2, 4],
                "expected_pain_trend": "Improving; pain with certain movements (coughing, bending)",
                "mobility": "Normal walking; avoid lifting >15 lbs",
                "wound_status": "Bruising fading; swelling decreasing",
                "key_instructions": [
                    "Return to desk work if comfortable",
                    "Continue avoiding heavy lifting and straining",
                    "Discontinue opioids",
                ],
            },
            {
                "phase": "days_8_21",
                "days": (8, 21),
                "expected_pain_range": [0, 2],
                "expected_pain_trend": "Minimal; occasional twinges are normal",
                "mobility": "Gradual return to full activity; heavy lifting at 3-4 weeks",
                "wound_status": "Healed incisions; mesh integration ongoing (internal)",
                "key_instructions": [
                    "Follow-up at 2 weeks",
                    "Resume exercise gradually at 2-3 weeks",
                    "Full activity clearance at 4 weeks post-op",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Increasing pain or new bulge at repair site (recurrence)",
            "Wound redness, swelling, or drainage",
            "Inability to pass gas or stool (bowel obstruction signs)",
            "Testicular pain or swelling that is worsening (inguinal repair)",
            "Urinary retention",
            "Chest pain or shortness of breath",
        ],
    },

    # ── 8. Robotic Colectomy ─────────────────────────────────────────────────

    "robotic_colectomy": {
        "display_name": "Robotic Colectomy",
        "aliases": [
            "robotic colectomy", "robot-assisted colectomy", "laparoscopic colectomy",
            "colon resection", "hemicolectomy", "sigmoidectomy", "bowel resection",
        ],
        "typical_recovery_days": 42,
        "typical_hospital_stay_days": 3,
        "typical_medications": ["Acetaminophen", "Oxycodone", "Enoxaparin", "Ondansetron", "Warfarin", "Docusate"],
        "timeline": [
            {
                "phase": "days_1_3",
                "days": (1, 3),
                "expected_pain_range": [4, 7],
                "expected_pain_trend": "Moderate abdominal pain; managed with multimodal analgesia",
                "mobility": "Walking in hospital by day 1 (ERAS protocol); short walks at home",
                "wound_status": "Port-site incisions; possible extraction site (4-6 cm); staples or sutures",
                "key_instructions": [
                    "Clear liquids → full liquids → soft diet progression",
                    "Walking is critical for bowel recovery",
                    "Incentive spirometry to prevent pneumonia",
                    "Monitor for return of bowel function (passing gas)",
                ],
            },
            {
                "phase": "days_4_7",
                "days": (4, 7),
                "expected_pain_range": [3, 5],
                "expected_pain_trend": "Improving; pain with coughing and movement",
                "mobility": "Walking longer distances; stairs with assistance",
                "wound_status": "Incisions drying; extraction site may be tender",
                "key_instructions": [
                    "Advance diet as tolerated — avoid high-fibre initially",
                    "Bowel function should be returning (passing gas, then stool)",
                    "Continue anticoagulation as prescribed",
                    "Transition to oral pain management",
                ],
            },
            {
                "phase": "days_8_14",
                "days": (8, 14),
                "expected_pain_range": [2, 4],
                "expected_pain_trend": "Steady improvement",
                "mobility": "Normal walking; avoid heavy lifting",
                "wound_status": "Healing well; staple removal at 10-14 days if applicable",
                "key_instructions": [
                    "Follow-up appointment — wound check and pathology results",
                    "Regular bowel movements should be establishing",
                    "Light work if non-physical",
                    "Gradual dietary normalisation",
                ],
            },
            {
                "phase": "days_15_42",
                "days": (15, 42),
                "expected_pain_range": [0, 2],
                "expected_pain_trend": "Minimal",
                "mobility": "Gradual return to full activity by 4-6 weeks",
                "wound_status": "Fully healed",
                "key_instructions": [
                    "Resume normal diet",
                    "Return to exercise at 4-6 weeks",
                    "Oncology follow-up if surgery was for cancer",
                    "Report any change in bowel habits",
                ],
            },
        ],
        "red_flags": [
            "Fever >38°C (100.4°F)",
            "Increasing abdominal pain or distension",
            "No passage of gas or stool for >3 days post-op (ileus signs)",
            "Persistent nausea/vomiting",
            "Wound redness, swelling, or purulent drainage",
            "Rectal bleeding (new or increasing)",
            "Signs of anastomotic leak: sudden severe pain, tachycardia, fever",
            "Chest pain or shortness of breath (PE signs)",
            "Calf swelling or tenderness (DVT signs)",
            "Easy bruising or bleeding (if on anticoagulation)",
        ],
    },
}


# ── Lookup helpers ─────────────────────────────────────────────────────────────

def find_procedure(name: str) -> dict | None:
    """
    Find a procedure by name or alias. Case-insensitive.
    Substring match in either direction so "Robotic Prostatectomy (da Vinci)"
    matches "robotic prostatectomy".
    """
    import re
    name_lower = re.sub(r"\s*\([^)]*\)", "", name or "").strip().lower()
    if not name_lower:
        return None

    if name_lower.replace(" ", "_") in PROCEDURES:
        return PROCEDURES[name_lower.replace(" ", "_")]

    for proc_data in PROCEDURES.values():
        display = proc_data["display_name"].lower()
        if name_lower == display or display in name_lower or name_lower in display:
            return proc_data
        for alias in proc_data["aliases"]:
            alias_lower = alias.lower()
            if name_lower == alias_lower or alias_lower in name_lower or name_lower in alias_lower:
                return proc_data

    return None


def get_expected_pain_range(procedure_name: str, post_op_day: int) -> tuple[int, int] | None:
    """
    Get the expected pain range [min, max] for a given procedure and post-op day.
    Returns None if procedure not found or day is out of range.
    """
    proc = find_procedure(procedure_name)
    if not proc:
        return None

    for phase in proc["timeline"]:
        start, end = phase["days"]
        if start <= post_op_day <= end:
            return tuple(phase["expected_pain_range"])

    return None


def get_timeline_phase(procedure_name: str, post_op_day: int) -> dict | None:
    """
    Get the full timeline phase data for a given procedure and post-op day.
    Returns None if procedure not found or day is out of range.
    """
    proc = find_procedure(procedure_name)
    if not proc:
        return None

    for phase in proc["timeline"]:
        start, end = phase["days"]
        if start <= post_op_day <= end:
            return phase

    return None


def get_red_flags(procedure_name: str) -> list[str]:
    """
    Get the red-flag symptoms for a given procedure.
    Returns an empty list if procedure not found.
    """
    proc = find_procedure(procedure_name)
    if not proc:
        return []
    return proc["red_flags"]


def list_procedure_names() -> list[str]:
    """Return display names of all supported procedures."""
    return [p["display_name"] for p in PROCEDURES.values()]
