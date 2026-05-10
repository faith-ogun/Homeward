"""
Patch each patient bundle with PGx Observation resources.

Each gene mentioned in the existing DiagnosticReport.conclusion becomes a
separate Observation. Belt-and-braces with the conclusion string so PGx
data is visible regardless of which FHIR projection (DiagnosticReport vs
Observation) the calling agent uses.

Run:
    python scripts/add_pgx_observations.py
"""
from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

PATIENTS_DIR = Path(__file__).parent.parent / "synthetic_data" / "patients"

GENE_PATTERN = re.compile(
    r"(CYP2D6|CYP2C19|CYP2C9|CYP3A4|VKORC1|DPYD|UGT1A1|TPMT|SLCO1B1)"
    r"\s*"
    r"((?:-?\d+\s*[A-Z]?>?[A-Z]?\s*)?(?:\*\w+\s*/\s*\*\w+|\*\w+|AA|AG|GG|GA|wild[- ]type))"
    r"(?:\s*\(([^)]+)\))?",
    re.IGNORECASE,
)

# LOINC codes for pharmacogenomic phenotype reporting
LOINC_GENOTYPE_DISPLAY = {"system": "http://loinc.org", "code": "84413-4", "display": "Genotype display name"}


def parse_pgx_conclusion(conclusion: str) -> list[dict]:
    """Parse 'CYP2D6 *4/*4 (Poor Metabolizer). CYP2C19 *1/*1 (Normal Metabolizer)...' into structured entries."""
    entries = []
    for m in GENE_PATTERN.finditer(conclusion or ""):
        gene = m.group(1).upper()
        diplotype = m.group(2).strip()
        phenotype = (m.group(3) or "").strip() or None
        entries.append({"gene": gene, "diplotype": diplotype, "phenotype": phenotype})
    return entries


def build_observation(
    *,
    patient_ref: str,
    effective_date: str,
    gene: str,
    diplotype: str,
    phenotype: str | None,
) -> dict:
    """Build a FHIR R4 Observation for one gene/diplotype call."""
    text_value = f"{diplotype}" + (f" ({phenotype})" if phenotype else "")
    resource: dict = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "laboratory",
                        "display": "Laboratory",
                    }
                ]
            }
        ],
        "code": {
            "coding": [LOINC_GENOTYPE_DISPLAY],
            "text": f"{gene} genotype",
        },
        "subject": {"reference": patient_ref},
        "effectiveDateTime": effective_date,
        "valueCodeableConcept": {"text": text_value},
        "note": [
            {"text": f"{gene} {diplotype}" + (f" — {phenotype}" if phenotype else "")}
        ],
    }
    # FHIR R4: array-valued fields must be omitted when empty (cannot be []).
    if phenotype:
        resource["interpretation"] = [{"text": phenotype}]

    return {
        "fullUrl": f"urn:uuid:{uuid.uuid4()}",
        "resource": resource,
        "request": {"method": "POST", "url": "Observation"},
    }


def patch_bundle(path: Path) -> int:
    bundle = json.loads(path.read_text())
    entries = bundle.get("entry", [])

    # Find the existing PGx DiagnosticReport
    pgx_report = None
    for e in entries:
        r = e.get("resource", {})
        if r.get("resourceType") == "DiagnosticReport":
            text = (r.get("code") or {}).get("text", "").lower()
            if any(kw in text for kw in ("pharmacogenomic", "pgx", "genetic")):
                pgx_report = r
                break
    if not pgx_report:
        print(f"  [skip] no PGx DiagnosticReport in {path.name}")
        return 0

    conclusion = pgx_report.get("conclusion") or ""
    parsed = parse_pgx_conclusion(conclusion)
    if not parsed:
        print(f"  [skip] could not parse conclusion in {path.name}")
        return 0

    patient_ref = (pgx_report.get("subject") or {}).get("reference", "")
    effective_date = pgx_report.get("effectiveDateTime") or "2026-04-20"

    # Drop any pre-existing PGx Observations from a previous run (idempotent)
    def is_existing_pgx_obs(e: dict) -> bool:
        r = e.get("resource", {})
        if r.get("resourceType") != "Observation":
            return False
        text = (r.get("code") or {}).get("text", "")
        return "genotype" in text.lower()

    entries = [e for e in entries if not is_existing_pgx_obs(e)]

    # Build new Observations
    new_obs = [
        build_observation(
            patient_ref=patient_ref,
            effective_date=effective_date,
            gene=p["gene"],
            diplotype=p["diplotype"],
            phenotype=p["phenotype"],
        )
        for p in parsed
    ]

    bundle["entry"] = entries + new_obs
    path.write_text(json.dumps(bundle, indent=2))
    return len(new_obs)


def main() -> None:
    files = sorted(PATIENTS_DIR.glob("patient_*.json"))
    print(f"Patching {len(files)} bundles in {PATIENTS_DIR}")
    for p in files:
        n = patch_bundle(p)
        print(f"  {p.name}: +{n} Observations")


if __name__ == "__main__":
    main()
