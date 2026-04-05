"""
Homeward — A2A application entry point.

Start the server with:
    uvicorn homeward.app:a2a_app --host 0.0.0.0 --port 8001

The agent card is served publicly at:
    GET http://localhost:8001/.well-known/agent-card.json

All other endpoints require an X-API-Key header (see shared/middleware.py).
"""
import os

from a2a.types import AgentSkill
from shared.app_factory import create_a2a_app

from .agent import root_agent

a2a_app = create_a2a_app(
    agent=root_agent,
    name="Homeward",
    description=(
        "Post-surgical recovery monitoring agent with pharmacogenomic medication "
        "review. Monitors patient recovery against procedure-specific expected "
        "timelines and flags drug-gene interactions in post-operative medications."
    ),
    url=os.getenv("HOMEWARD_URL", os.getenv("BASE_URL", "http://localhost:8001")),
    port=8001,
    fhir_extension_uri=f"{os.getenv('PO_PLATFORM_BASE_URL', 'https://app.promptopinion.ai')}/schemas/a2a/v1/fhir-context",
    skills=[
        AgentSkill(
            id="discharge_note_interpreter",
            name="Discharge Note Interpreter",
            description=(
                "Reads discharge instructions and FHIR patient context to produce "
                "structured recovery expectations including procedure-specific timelines, "
                "medication schedules, and red-flag symptoms."
            ),
            tags=["discharge", "recovery", "post-op", "surgery"],
        ),
        AgentSkill(
            id="pharmacogenomic_medication_review",
            name="Pharmacogenomic Medication Review",
            description=(
                "Checks post-operative medications against patient pharmacogenomic "
                "profile and flags drug-gene interactions with CPIC-guided alternative "
                "recommendations."
            ),
            tags=["pharmacogenomics", "medication", "drug-gene", "PGx", "CPIC"],
        ),
        AgentSkill(
            id="recovery_check_in_assessment",
            name="Recovery Check-In Assessment",
            description=(
                "Compares patient-reported symptoms against procedure-specific expected "
                "recovery timeline and pharmacogenomic context. Returns on-track, watch, "
                "or escalate classification."
            ),
            tags=["recovery", "check-in", "symptoms", "monitoring"],
        ),
        AgentSkill(
            id="escalation_summary_generator",
            name="Escalation Summary Generator",
            description=(
                "Generates structured GREEN/AMBER/RED clinical summary combining "
                "recovery assessment, pharmacogenomic flags, and recommended actions "
                "for care team and patient."
            ),
            tags=["escalation", "summary", "alert", "clinical"],
        ),
    ],
)
