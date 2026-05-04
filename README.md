# Homeward

**The only post-surgical recovery agent that thinks about pharmacogenomics.**

An A2A agent for [Prompt Opinion](https://app.promptopinion.ai) that monitors patient recovery against procedure-specific timelines AND flags drug-gene interactions in post-operative medications. When a patient reports uncontrolled pain, Homeward tells you whether it's a surgical complication or a pharmacogenomic mismatch — a clinical insight no other agent in this hackathon's field produces.

Built for [Agents Assemble — The Healthcare AI Endgame](https://agents-assemble.devpost.com/) hackathon.

**Live agent:** `https://homeward-434257808344.us-central1.run.app`
**Agent card:** `https://homeward-434257808344.us-central1.run.app/.well-known/agent-card.json`

---

## The Problem

### Two Blind Spots in Post-Surgical Care

**Blind Spot 1 — Post-discharge recovery.** Patients go home 24–48 hours after minimally invasive or robotic surgery with paper discharge instructions and no structured clinical visibility until their follow-up appointment 2–4 weeks later. Over 80% of surgery is now outpatient. Complications — infection, thrombosis, wound dehiscence — develop in that monitoring gap. Post-operative complications are the third leading cause of death worldwide.

**Blind Spot 2 — Pharmacogenomic medication risk.** Post-surgical patients are prescribed pain management (opioids, NSAIDs), anticoagulants, antibiotics, anti-emetics. ~99% of people carry at least one actionable pharmacogenomic variant. A CYP2D6 poor metabolizer prescribed codeine for post-op pain gets no analgesic effect because they cannot convert codeine to morphine. A CYP2C19 rapid metabolizer on clopidogrel after a cardiac procedure may still form clots. Known, preventable problems that are rarely checked at discharge.

**Why they belong together.** The medication check is not a separate feature — it is part of the recovery assessment. If a patient reports uncontrolled pain on day 3, the answer might not be "this is abnormal, escalate" — it might be "this patient is a CYP2D6 poor metabolizer on codeine; the drug is not working for them; recommend switching to an alternative analgesic." That is a fundamentally different clinical insight than either system produces alone.

---

## How It Works

Homeward is a single external A2A agent exposing five skills, consultable from any clinician workspace in Prompt Opinion.

### The Five Skills

| Skill | What It Does |
|-------|-------------|
| **Discharge Note Interpreter** | Reads discharge instructions and FHIR patient context to produce structured recovery expectations — procedure-specific timelines, medication schedules, red-flag symptoms |
| **Pharmacogenomic Medication Review** | Checks post-operative medications against the patient's pharmacogenomic profile and flags drug-gene interactions with CPIC-guided alternative recommendations |
| **Recovery Check-In Assessment** | Compares patient-reported symptoms against procedure-specific expected recovery trajectory and pharmacogenomic context — returns on-track / watch / escalate classification |
| **Escalation Summary Generator** | Generates structured GREEN / AMBER / RED clinical summary combining recovery assessment, pharmacogenomic flags, and recommended actions for the care team |
| **FHIR Action Drafter** | When a pharmacogenomic alternative is warranted, drafts FHIR R4 resources (MedicationRequest + Communication) with `status="draft"` / `intent="proposal"` for clinician review — never auto-submits, never auto-prescribes |

### Clinical Data Sources

| Source | What It Provides |
|--------|-----------------|
| [CPIC Guidelines](https://cpicpgx.org/guidelines/) | Evidence-based drug-gene interaction recommendations (9 drugs, 5 genes) |
| [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) | Pre-cached variant clinical significance for ~30 PGx star alleles |
| Procedure-specific recovery timelines | Deterministic expected pain curves, mobility milestones, red flags for 8 procedures |

Recovery timelines and drug-gene matching are **deterministic** — sourced from published clinical guidelines, not LLM-generated. The LLM (Gemini 2.5 Flash) interprets discharge notes, explains PGx findings in plain language, and synthesises the final assessment.

### Example — Patient 001 (the demo)

> A patient had a robotic prostatectomy 4 days ago. They report pain 7/10, not improving. They're prescribed codeine. Their FHIR record contains a pharmacogenomic panel.
>
> **Generic recovery agent:** *"Pain is above expected range for day 4. Recommend clinical review."*
>
> **Homeward:** *"Pain is above expected range for day 4. This patient is a CYP2D6 poor metabolizer (\*4/\*4, ClinVar Pathogenic). Codeine requires CYP2D6-mediated conversion to morphine for analgesic effect — this patient will experience significantly reduced or no pain relief. The elevated pain is likely pharmacogenomic in origin, not a surgical complication. Recommend switching to oxycodone or a non-opioid alternative per CPIC guideline (Crews et al., 2021)."*

---

## Architecture

```
Prompt Opinion Workspace
    │  Clinician selects patient → general chat agent → consults Homeward
    ▼
Homeward (A2A request, Cloud Run)
    │  FHIR token + patientId arrive in message.metadata
    ▼
Pull patient context from FHIR
    ├── Procedure (computes post-op day from performed_date)
    ├── Active medications
    ├── PGx panel — diplotypes parsed from DiagnosticReport conclusion
    └── Conditions, observations
    ▼
Run the five skills in sequence
    ├── Deterministic data (recovery timelines, CPIC drug-gene table, ClinVar, red flags)
    └── LLM (Gemini 2.5 Flash) for interpretation and synthesis
    ▼
Return structured A2A Task envelope
    ├── Recovery assessment (on track / deviation detected)
    ├── PGx flags with CPIC + ClinVar citations
    ├── Escalation level (GREEN / AMBER / RED)
    └── Care-team and patient-facing guidance
```

### Tech stack

| Layer | Technology |
|-------|-----------|
| Agent framework | [Google ADK](https://google.github.io/adk-docs/) (Python) |
| A2A protocol | JSON-RPC 2.0 over HTTP, A2A v1 spec |
| LLM | Gemini 2.5 Flash via Google AI Studio (free tier) |
| FHIR integration | [SHARP-on-MCP](https://sharponmcp.com/) context propagation |
| PGx evidence | CPIC Guidelines + pre-cached ClinVar |
| Hosting | Google Cloud Run (region `us-central1`) |
| Platform | [Prompt Opinion](https://app.promptopinion.ai) |

Built from the [po-adk-python](https://github.com/prompt-opinion/po-adk-python) template, with a custom translation middleware in `shared/middleware.py` that handles PO-specific request/response shape (PascalCase JSON-RPC method names, proto-style enums, A2A v1 nested-key security schemes, and the `result.task` wrapper).

---

## Supported Procedures

Eight common minimally invasive / robotic procedures, each with deterministic expected pain trajectory, mobility milestones, wound healing stages, and procedure-specific red flags:

Robotic prostatectomy · Laparoscopic cholecystectomy · Total knee replacement · Robotic hysterectomy · Laparoscopic appendectomy · Robotic partial nephrectomy · Laparoscopic hernia repair · Robotic colectomy

## Drug-Gene Pairs

| Drug | Gene(s) | Post-Surgical Relevance |
|------|---------|------------------------|
| Codeine | CYP2D6 | PMs get no pain relief; UMs risk toxicity |
| Tramadol | CYP2D6 | Prodrug requiring CYP2D6 activation |
| Oxycodone | CYP2D6 | Partial CYP2D6 metabolism |
| Celecoxib | CYP2C9 | PMs have increased exposure, GI/CV risk |
| Ibuprofen | CYP2C9 | PMs have increased exposure |
| Warfarin | CYP2C9 + VKORC1 | Dose-sensitive; variants drive bleeding risk |
| Clopidogrel | CYP2C19 | PMs have reduced antiplatelet effect |
| Ondansetron | CYP2D6 | UMs may have reduced antiemetic effect |
| Fluorouracil | DPYD | PMs risk severe / fatal toxicity |

All recommendations cite [CPIC guidelines](https://cpicpgx.org/guidelines/).

---

## Quick Start (local development)

### Prerequisites

- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (free)
- ngrok or any HTTPS tunnel for local PO connection

### Setup

```bash
git clone https://github.com/faith-ogun/Homeward.git
cd Homeward
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set GOOGLE_API_KEY + HOMEWARD_API_KEY
```

### Run

```bash
uvicorn homeward.app:a2a_app --host 0.0.0.0 --port 8001 --reload
```

In a second terminal:

```bash
ngrok http 8001
```

Verify the agent card:

```bash
curl https://<your-ngrok-url>/.well-known/agent-card.json | jq .name
# → "Homeward"
```

### Connect to Prompt Opinion

1. **Workspace Hub** → External Agents → **Add Connection**
2. Paste the ngrok URL (the base, no trailing slash)
3. Click **Check** — PO pulls the agent card and shows the five skills
4. Set the API key (value of `HOMEWARD_API_KEY` from `.env`)
5. Enable **FHIR R4 context** and select **Full Authority** under Patient Data Permissions
6. **Save**
7. Launchpad → select a patient → general chat → consult Homeward

---

## Production deploy (Cloud Run)

The live demo runs on Cloud Run. Full deploy command and ops cheat sheet are in `deployment.txt` (local-only, gitignored). Summary:

```bash
GOOGLE_API_KEY=$(grep -E "^GOOGLE_API_KEY=" .env | cut -d= -f2 | tr -d '"' | tr -d "'")
HOMEWARD_API_KEY=$(grep -E "^HOMEWARD_API_KEY=" .env | cut -d= -f2 | tr -d '"' | tr -d "'")
URL="https://homeward-434257808344.us-central1.run.app"

gcloud run deploy homeward \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 5 \
  --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY},GOOGLE_GENAI_USE_VERTEXAI=FALSE,HOMEWARD_API_KEY=${HOMEWARD_API_KEY},BASE_URL=${URL},HOMEWARD_URL=${URL}"
```

Pinned versions in `requirements.txt` — do not loosen them. `google-adk 1.18.0` and `a2a-sdk[http-server] 0.3.22` are the working combination; later releases changed import paths.

---

## Project Structure

```
.
├── homeward/                       The Homeward A2A agent
│   ├── agent.py                    Root agent — model, instruction, tools
│   ├── app.py                      A2A app — agent card, skills, entry point
│   └── tools/
│       ├── discharge.py            Skill 1 — Discharge Note Interpreter
│       ├── pgx.py                  Skill 2 — Pharmacogenomic Medication Review
│       ├── recovery.py             Skill 3 — Recovery Check-In Assessment
│       ├── escalation.py           Skill 4 — Escalation Summary Generator
│       └── action_drafter.py       Skill 5 — FHIR Action Drafter
│
├── shared/                         Platform-shim / infra layer
│   ├── app_factory.py              A2A ASGI app builder, agent card construction
│   ├── middleware.py               PO ↔ A2A translation: method/role/role rewrites,
│   │                               agent card patching, response Task-wrapping,
│   │                               API key auth
│   ├── fhir_hook.py                FHIR credential extraction → session state,
│   │                               with deep-search fallback for ADK quirks
│   ├── logging_utils.py            Redaction + safe JSON serialisation
│   └── tools/
│       └── fhir.py                 FHIR R4 query tools (Patient, Procedure,
│                                   MedicationRequest, DiagnosticReport,
│                                   Condition, Observation)
│
├── data/                           Deterministic clinical reference data
│   ├── procedures.py               8 procedures × recovery timelines
│   ├── drug_gene_pairs.py          9 CPIC drug-gene pairs
│   ├── clinvar.py                  ~30 PGx star allele classifications
│   └── red_flags.py                Universal post-op red flag rules
│
├── synthetic_data/                 Demo patients (no real PHI)
│   ├── patients/                   FHIR transaction Bundles (4 patients)
│   ├── discharge_notes/            Plain-text discharge instructions
│   └── genomic_profiles/           Structured PGx reports (reference)
│
├── Dockerfile                      Cloud Run container image
├── Procfile                        Process definition
├── requirements.txt                Pinned Python dependencies
├── .env.example                    Environment variable template
└── README.md                       This file
```

---

## Safety & Privacy

- All patient data used in development and demonstration is **synthetic** — no real PHI
- PGx recommendations are **informational**, citing CPIC guidelines — not autonomous prescribing decisions
- Recovery assessments **defer to the care team** — the agent recommends clinical review, it does not diagnose
- Escalation is **advisory, not diagnostic** — GREEN / AMBER / RED classification with reasoning and recommended actions
- Operates as a **clinical decision support tool** consulted by other agents within a professional workspace — not a patient-facing application
- FHIR credentials are handled securely — extracted from A2A metadata into session state, never written to LLM prompts
- API key authentication on all non-public endpoints; agent card is the only unauthenticated route

### Future directions

- Consume `Observation` and `MolecularSequence` per CPIC structured-panel format (currently parses diplotypes from DiagnosticReport conclusion text)
- Persistent session memory for multi-day pain trajectory tracking
- FHIR `ServiceRequest` / `Communication` output back to the EHR
- Integration with institutional pharmacogenomic testing workflows (Mayo, Cleveland Clinic both run active PGx programs)
- SMART on FHIR launch context
- Clinical validation study with surgical teams
- Expansion to additional procedures and drug-gene pairs

---

## Built With

[Google ADK](https://google.github.io/adk-docs/) · [A2A Protocol](https://a2aprotocol.ai/) · [Prompt Opinion](https://promptopinion.ai) · [SHARP-on-MCP](https://sharponmcp.com/) · [CPIC](https://cpicpgx.org/) · [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) · [Gemini](https://aistudio.google.com/) · [Google Cloud Run](https://cloud.google.com/run)

---

## Author

**Faith Ogundimu** — PhD student in Cancer Genomics / Bioinformatics

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
