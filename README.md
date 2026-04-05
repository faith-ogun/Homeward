# Homeward

**Post-surgical recovery monitoring with pharmacogenomic medication review.**

An A2A agent for [Prompt Opinion](https://app.promptopinion.ai) that monitors patient recovery against procedure-specific timelines and flags drug-gene interactions in post-operative medications.

Built for [Agents Assemble — The Healthcare AI Endgame](https://agents-assemble.devpost.com/) hackathon.

---

## The Problem

### Two Blind Spots in Post-Surgical Care

**Blind Spot 1: Post-Discharge Recovery**

Patients go home 24–48 hours after minimally invasive or robotic surgery with paper discharge instructions and no structured clinical visibility until their follow-up appointment 2–4 weeks later. Over 80% of surgery is now outpatient. Complications — infection, thrombosis, wound dehiscence — develop in that monitoring gap. Post-operative complications are the third leading cause of death worldwide.

**Blind Spot 2: Pharmacogenomic Medication Risk**

Post-surgical patients are prescribed pain management (opioids, NSAIDs), anticoagulants, antibiotics, and anti-emetics. ~99% of people carry at least one actionable pharmacogenomic variant. A CYP2D6 poor metabolizer prescribed codeine for post-op pain gets no analgesic effect because they cannot convert codeine to morphine. A CYP2C19 rapid metabolizer on clopidogrel after a cardiac procedure may still form clots. These are known, preventable problems that are rarely checked at discharge.

**Why They Belong Together**

The medication check is not a separate feature — it is part of the recovery assessment. If a patient reports uncontrolled pain on day 3, the answer might not be "this is abnormal, escalate" — it might be "this patient is a CYP2D6 poor metabolizer on codeine; the drug is not working for them; recommend switching to an alternative analgesic." That is a fundamentally different clinical insight than either system produces alone.

---

## How It Works

Homeward is a single external A2A agent that exposes four skills, consultable from any clinician workspace in Prompt Opinion.

### The Four Skills

| Skill | What It Does |
|-------|-------------|
| **Discharge Note Interpreter** | Reads discharge instructions and FHIR patient context to produce structured recovery expectations — procedure-specific timelines, medication schedules, and red-flag symptoms |
| **Pharmacogenomic Medication Review** | Checks post-operative medications against the patient's pharmacogenomic profile and flags drug-gene interactions with CPIC-guided alternative recommendations |
| **Recovery Check-In Assessment** | Compares patient-reported symptoms against procedure-specific expected recovery trajectory and pharmacogenomic context — returns on-track / watch / escalate classification |
| **Escalation Summary Generator** | Generates structured GREEN / AMBER / RED clinical summary combining recovery assessment, pharmacogenomic flags, and recommended actions for the care team |

### Clinical Data Sources

| Source | What It Provides |
|--------|-----------------|
| [CPIC Guidelines](https://cpicpgx.org/guidelines/) | Evidence-based drug-gene interaction recommendations |
| [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) | Variant clinical significance classification (pathogenic / VUS / benign) |
| Procedure-specific recovery timelines | Deterministic expected pain curves, mobility milestones, red-flag symptoms for common surgical procedures |

Recovery timelines and drug-gene matching are **deterministic** — sourced from published clinical guidelines, not LLM-generated. The LLM is used for interpreting discharge notes, explaining PGx findings in plain language, and synthesising contextualised assessments.

### Example Scenario

> A patient had a robotic prostatectomy 4 days ago. They report pain 7/10, not improving. They're prescribed codeine for pain management.
>
> **Without Homeward:** "Pain is above expected range for day 4. Recommend clinical review."
>
> **With Homeward:** "Pain is above expected range for day 4. However, this patient is a CYP2D6 poor metabolizer (\*4/\*4). Codeine requires CYP2D6-mediated conversion to morphine for analgesic effect — this patient will experience significantly reduced or no pain relief. The elevated pain is likely pharmacogenomic in origin, not a surgical complication. Recommend switching to oxycodone or a non-opioid alternative per CPIC guideline."

---

## Architecture

```
Prompt Opinion Workspace
    │
    │  Clinician selects patient → launches general agent → consults Homeward
    │
    ▼
Homeward receives A2A request with FHIR context:
    ├── Patient demographics, procedures, medications (via FHIR)
    ├── Genomic variants / PGx profile (via FHIR or uploaded report)
    ├── Uploaded discharge instructions
    └── Natural language query from the consulting agent
    │
    ▼
Homeward processes using:
    ├── Deterministic clinical logic (recovery timelines, drug-gene pairs, red flags)
    ├── CPIC/ClinVar evidence base (curated, not hallucinated)
    └── LLM reasoning (discharge interpretation, PGx explanation, assessment synthesis)
    │
    ▼
Homeward returns structured response:
    ├── Recovery assessment (on track / deviation detected)
    ├── PGx flags with CPIC citations (if drug-gene interactions found)
    ├── Escalation level (GREEN / AMBER / RED)
    ├── Recommended actions
    └── Clinical reasoning
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | [Google ADK](https://google.github.io/adk-docs/) (Python) |
| A2A Protocol | JSON-RPC 2.0 over HTTP ([A2A spec](https://a2aprotocol.ai/)) |
| LLM | Gemini Flash via Google AI Studio |
| FHIR Integration | [SHARP-on-MCP](https://sharponmcp.com/) context propagation |
| PGx Evidence | CPIC Guidelines + ClinVar |
| Hosting | Google Cloud Run |
| Platform | [Prompt Opinion](https://app.promptopinion.ai) |

Built from the [po-adk-python](https://github.com/prompt-opinion/po-adk-python) template.

---

## Supported Procedures

Homeward tracks recovery for common minimally invasive and robotic procedures:

- Robotic Prostatectomy
- Laparoscopic Cholecystectomy
- Total Knee Replacement (robotic-assisted)
- Robotic Hysterectomy
- Laparoscopic Appendectomy
- Robotic Partial Nephrectomy
- Laparoscopic Hernia Repair
- Robotic Colectomy

Each procedure has defined expected pain trajectories, mobility milestones, wound healing stages, and procedure-specific red-flag symptoms.

## Key Drug-Gene Pairs

| Drug | Gene(s) | Post-Surgical Relevance |
|------|---------|------------------------|
| Codeine | CYP2D6 | Poor metabolizers get no pain relief; ultrarapid metabolizers risk toxicity |
| Tramadol | CYP2D6 | Prodrug requiring CYP2D6 activation |
| Oxycodone | CYP2D6 | Partial CYP2D6 metabolism |
| Celecoxib | CYP2C9 | Poor metabolizers have increased exposure and GI/CV risk |
| Warfarin | CYP2C9, VKORC1 | Dose-sensitive; variants cause bleeding risk |
| Clopidogrel | CYP2C19 | Poor metabolizers have reduced antiplatelet effect |
| Ondansetron | CYP2D6 | Ultrarapid metabolizers may have reduced antiemetic effect |
| Ibuprofen | CYP2C9 | Poor metabolizers have increased exposure |

All recommendations cite [CPIC guidelines](https://cpicpgx.org/guidelines/).

---

## Quick Start

### Prerequisites

- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (free)

### 1. Clone and set up

```bash
git clone https://github.com/faith-ogun/Homeward.git
cd Homeward
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your Google API key:

```env
GOOGLE_API_KEY=your-key-here
```

### 3. Run locally

```bash
uvicorn homeward.app:a2a_app --host 0.0.0.0 --port 8001
```

### 4. Verify the agent card

```bash
curl http://localhost:8001/.well-known/agent-card.json
```

### 5. Connect to Prompt Opinion

For local development, expose via ngrok:

```bash
ngrok http 8001
```

Then in Prompt Opinion:
1. Go to **Workspace Hub** → Add external agent
2. Paste the agent card URL: `https://<your-ngrok-url>/.well-known/agent-card.json`
3. Enter your API key
4. Enable FHIR context
5. Save and test from the Launchpad

### Deploy to Cloud Run (production)

```bash
gcloud run deploy homeward \
  --source . \
  --region us-central1 \
  --set-env-vars "AGENT_MODULE=homeward.app:a2a_app,GOOGLE_GENAI_USE_VERTEXAI=FALSE" \
  --set-secrets "GOOGLE_API_KEY=google-api-key:latest" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 3
```

---

## Project Structure

```
├── homeward/                # The Homeward A2A agent
│   ├── __init__.py
│   ├── agent.py             # Root agent: model, instruction, tools
│   ├── app.py               # A2A app: agent card, skills, entry point
│   └── tools/               # Skill implementations
│       ├── discharge.py     # Discharge Note Interpreter
│       ├── pgx.py           # Pharmacogenomic Medication Review
│       ├── recovery.py      # Recovery Check-In Assessment
│       └── escalation.py    # Escalation Summary Generator
│
├── shared/                  # Infrastructure (from po-adk-python template)
│   ├── app_factory.py       # A2A ASGI app builder
│   ├── fhir_hook.py         # FHIR credential extraction → session state
│   ├── middleware.py        # API key authentication
│   ├── logging_utils.py     # Logging utilities
│   └── tools/
│       └── fhir.py          # FHIR R4 query tools
│
├── data/                    # Clinical reference data
├── tests/                   # Tests
├── Dockerfile               # Container image
├── Procfile                 # Process definition
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variable template
```

---

## Safety & Privacy

- All patient data used in development and demonstration is **synthetic** — no real PHI
- PGx recommendations are **informational**, citing CPIC guidelines — not autonomous prescribing decisions
- Recovery assessments **defer to the care team** — the agent recommends clinical review, it does not diagnose
- Escalation is **advisory, not diagnostic** — GREEN / AMBER / RED classification with reasoning and recommended actions
- The agent operates as a **clinical decision support tool** consulted by other agents within a professional workspace — it is not a patient-facing application
- FHIR credentials are handled securely — extracted from A2A metadata into session state, never appearing in LLM prompts

### Future Directions

- On-device or local inference for stronger data privacy
- Integration with institutional pharmacogenomic testing workflows
- EHR integration via SMART on FHIR launch context
- Clinical validation study with surgical teams
- Expansion to additional procedures and drug-gene pairs
- Multi-language support for diverse patient populations

---

## Built With

- [Google ADK](https://google.github.io/adk-docs/) — Agent Development Kit
- [A2A Protocol](https://a2aprotocol.ai/) — Agent-to-Agent communication
- [Prompt Opinion](https://promptopinion.ai) — Multi-agent healthcare platform
- [SHARP-on-MCP](https://sharponmcp.com/) — Healthcare context propagation
- [CPIC](https://cpicpgx.org/) — Clinical Pharmacogenetics Implementation Consortium
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) — Genomic variant classification
- [Gemini](https://aistudio.google.com/) — Large language model
- [Google Cloud Run](https://cloud.google.com/run) — Serverless deployment

---

## Author

**Faith Ogundimu** — PhD student in Cancer Genomics / Bioinformatics

---

## License

[MIT](LICENSE)
