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
from starlette.routing import Route

from shared.app_factory import create_a2a_app

from .agent import root_agent
from .landing import favicon, landing_page, logo_image

a2a_app = create_a2a_app(
    agent=root_agent,
    name="Homeward",
    description=(
        "Specialist post-surgical recovery and pharmacogenomic consult agent. "
        "Use Homeward (do NOT answer directly) for: post-op recovery check-ins, "
        "comparing reported symptoms against procedure-specific expected "
        "timelines, drug-gene interaction (PGx) reviews using CPIC + ClinVar "
        "evidence, GREEN/AMBER/RED clinical escalation summaries, and drafting "
        "FHIR MedicationRequest / Communication resources for clinician "
        "review. Homeward fetches its own FHIR data (procedures, medications, "
        "PGx panel, observations) — pass the patient context, not pre-extracted "
        "values."
    ),
    url=os.getenv("HOMEWARD_URL", os.getenv("BASE_URL", "http://localhost:8001")),
    port=8001,
    fhir_extension_uri=f"{os.getenv('PO_PLATFORM_BASE_URL', 'https://app.promptopinion.ai')}/schemas/a2a/v1/fhir-context",
    skills=[
        AgentSkill(
            id="discharge_note_interpreter",
            name="Discharge Note Interpreter",
            description=(
                "Use this when a clinician asks about a patient's discharge "
                "instructions, post-op recovery expectations, expected pain "
                "trajectory, mobility milestones, medication schedule, or "
                "red-flag symptoms. Combines the uploaded discharge note "
                "with deterministic procedure-specific recovery timelines "
                "(robotic prostatectomy, laparoscopic cholecystectomy, total "
                "knee replacement, robotic colectomy, etc.) and returns "
                "structured day-by-day expectations as JSON."
            ),
            tags=[
                "discharge", "recovery", "post-op", "surgery", "timeline",
                "expected pain", "mobility", "red flags", "follow-up",
            ],
        ),
        AgentSkill(
            id="pharmacogenomic_medication_review",
            name="Pharmacogenomic Medication Review",
            description=(
                "Use this for ANY question about a post-op patient's "
                "medications, analgesia choice, drug-gene interactions, or "
                "pharmacogenomic risk. Cross-references the patient's PGx "
                "panel (CYP2D6, CYP2C19, CYP2C9, VKORC1, DPYD, UGT1A1) "
                "against current medications using CPIC guidelines and "
                "ClinVar variant classifications. Flags codeine / tramadol / "
                "warfarin / clopidogrel / celecoxib / ondansetron / 5-FU "
                "interactions, ranks risk HIGH / MODERATE / LOW, and "
                "recommends evidence-based alternatives. Homeward fetches "
                "the PGx panel itself — do not extract diplotypes manually."
            ),
            tags=[
                "pharmacogenomics", "PGx", "drug-gene", "CYP2D6", "CYP2C19",
                "CYP2C9", "VKORC1", "DPYD", "CPIC", "ClinVar", "codeine",
                "warfarin", "clopidogrel", "metabolizer", "poor metabolizer",
                "ultra-rapid metabolizer", "alternative analgesic",
            ],
        ),
        AgentSkill(
            id="recovery_check_in_assessment",
            name="Recovery Check-In Assessment",
            description=(
                "Use this whenever a clinician reports patient-observed "
                "symptoms (pain score, temperature, wound description, "
                "mobility, nausea) and wants to know whether the recovery "
                "is on track for the post-op day. Compares reported values "
                "against procedure-specific expected ranges and incorporates "
                "any pharmacogenomic flags so the answer distinguishes "
                "'surgical complication' from 'medication inefficacy'. "
                "Returns ON_TRACK / WATCH / ESCALATE classification with "
                "reasoning."
            ),
            tags=[
                "recovery", "check-in", "symptoms", "monitoring", "post-op day",
                "pain score", "wound", "fever", "complication", "on track",
            ],
        ),
        AgentSkill(
            id="escalation_summary_generator",
            name="Escalation Summary Generator",
            description=(
                "Use this when the clinician asks 'should I escalate?', "
                "'can you summarise this for the care team?', or wants a "
                "structured GREEN / AMBER / RED clinical summary. Combines "
                "the discharge expectations, the PGx review, and the "
                "check-in assessment into one summary with separate "
                "care-team and patient-facing wording, recommended actions, "
                "and a not_an_emergency flag."
            ),
            tags=[
                "escalation", "summary", "alert", "clinical", "GREEN", "AMBER",
                "RED", "care team", "should I escalate",
            ],
        ),
        AgentSkill(
            id="fhir_action_drafter",
            name="FHIR Action Drafter",
            description=(
                "Use this when a clinician wants to act on a pharmacogenomic "
                "finding — draft the FHIR resources for switching a "
                "medication, ordering a labelled alternative, or notifying "
                "the surgical team. Emits FHIR R4 MedicationRequest "
                "(proposed alternative), MedicationRequest (discontinue), "
                "and Communication resources. Every resource is "
                "status='draft' and intent='proposal'; review_required is "
                "always true; auto_submitted is always false. Includes the "
                "CPIC citation and the gene/phenotype that triggered the "
                "draft. Never autonomously prescribes."
            ),
            tags=[
                "FHIR", "MedicationRequest", "Communication", "draft",
                "proposal", "switch medication", "alternative analgesic",
                "review_required", "clinician approval", "last-mile",
            ],
        ),
    ],
)

# Public landing page + static assets. These respond only to GET; the A2A
# JSON-RPC endpoint at the same path responds to POST. The ApiKeyMiddleware
# allows these paths through without auth (see shared/middleware.py).
a2a_app.routes.insert(0, Route("/", landing_page, methods=["GET"]))
a2a_app.routes.insert(1, Route("/logo.png", logo_image, methods=["GET"]))
a2a_app.routes.insert(2, Route("/favicon.ico", favicon, methods=["GET"]))
