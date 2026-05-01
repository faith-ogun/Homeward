"""
Skill 2: Pharmacogenomic Medication Review

Checks post-operative medications against the patient's pharmacogenomic profile
and flags drug-gene interactions with CPIC-guided alternative recommendations.

Clinical logic is deterministic — uses curated CPIC drug-gene tables and
pre-cached ClinVar classifications. The LLM consuming this tool's output is
responsible for plain-language clinical synthesis.
"""
import logging
import re

from google.adk.tools import ToolContext

from data.clinvar import classify_diplotype, get_variant_classification
from data.drug_gene_pairs import DRUG_GENE_PAIRS, check_interaction, find_drug_gene_pair

logger = logging.getLogger(__name__)


# ── Parsing helpers ───────────────────────────────────────────────────────────

_VARIANT_PATTERN = re.compile(
    r"(CYP\d+[A-Z]?\d*|VKORC1|DPYD|UGT1A1|TPMT|SLCO1B1)"  # gene
    r"\s*"
    r"([*\w./>\-+\d() ]+)",                                # allele/genotype string
    re.IGNORECASE,
)


def _parse_pgx_variants(pgx_variants: str) -> list[dict]:
    """
    Parse a free-text PGx variant string into structured gene/diplotype entries.

    Examples accepted:
        "CYP2D6 *4/*4, CYP2C19 *1/*1"
        "CYP2C9 *2/*3; VKORC1 AG"
        "CYP2D6 *4/*4"

    Returns list of {gene, diplotype, allele1, allele2} (allele2 may be None
    for non-star-allele genotypes like VKORC1 AG).
    """
    if not pgx_variants or pgx_variants.strip().lower() in ("unknown", "none", "n/a", ""):
        return []

    parsed = []
    chunks = re.split(r"[,;]+", pgx_variants)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        # Try to find gene + allele pattern
        m = re.match(r"([A-Z0-9]+)\s+(.+)", chunk, re.IGNORECASE)
        if not m:
            continue
        gene = m.group(1).upper()
        rest = m.group(2).strip()

        # VKORC1 special: genotypes like "AG", "AA", "GG" or "-1639G>A AG"
        if gene == "VKORC1":
            geno_match = re.search(r"\b(AA|AG|GA|GG)\b", rest)
            if geno_match:
                geno = geno_match.group(1).upper().replace("GA", "AG")
                parsed.append({
                    "gene": "VKORC1",
                    "diplotype": geno,
                    "allele1": geno,
                    "allele2": None,
                    "raw": chunk,
                })
            continue

        # Star allele diplotype: "*4/*4" or "*1/*17"
        star_match = re.search(r"(\*\w+)\s*/\s*(\*\w+)", rest)
        if star_match:
            parsed.append({
                "gene": gene,
                "diplotype": f"{star_match.group(1)}/{star_match.group(2)}",
                "allele1": star_match.group(1),
                "allele2": star_match.group(2),
                "raw": chunk,
            })
            continue

        # Single star allele
        single = re.search(r"(\*\w+)", rest)
        if single:
            parsed.append({
                "gene": gene,
                "diplotype": single.group(1),
                "allele1": single.group(1),
                "allele2": None,
                "raw": chunk,
            })

    return parsed


def _parse_medications(medications: str) -> list[str]:
    """Split a medication string into individual drug names (with dose)."""
    if not medications:
        return []
    items = [m.strip() for m in re.split(r"[,;\n]+", medications) if m.strip()]
    return items


def _extract_drug_name(med_string: str) -> str:
    """Extract the drug name from a string like 'Codeine 30mg' → 'Codeine'."""
    return re.split(r"\s+\d", med_string, maxsplit=1)[0].strip()


# ── Phenotype resolution ──────────────────────────────────────────────────────

def _resolve_phenotype(parsed_variant: dict) -> dict:
    """
    Convert a parsed variant entry into a phenotype + ClinVar classification.

    Returns dict with: gene, diplotype, phenotype, clinvar_classification,
    clinvar_variation_id, allele_details.
    """
    gene = parsed_variant["gene"]
    allele1 = parsed_variant["allele1"]
    allele2 = parsed_variant["allele2"]

    # VKORC1 — direct genotype lookup
    if gene == "VKORC1":
        key = f"VKORC1 -1639G>A ({allele1})"
        data = get_variant_classification(key)
        if data:
            phenotype_map = {
                "GG": "Normal Sensitivity",
                "AG": "Intermediate Sensitivity",
                "AA": "High Sensitivity",
            }
            return {
                "gene": "VKORC1",
                "diplotype": allele1,
                "phenotype": phenotype_map.get(allele1, "Unknown"),
                "clinvar_classification": data["clinical_significance"],
                "clinvar_variation_id": data["clinvar_variation_id"],
                "function": data["function"],
                "description": data["description"],
            }
        return {
            "gene": "VKORC1",
            "diplotype": allele1,
            "phenotype": "Unknown",
            "clinvar_classification": "Unknown",
        }

    # Star allele genes — use diplotype classification
    if allele2:
        result = classify_diplotype(gene, allele1, allele2)
        sig1 = result["allele1"].get("clinical_significance", "Unknown")
        sig2 = result["allele2"].get("clinical_significance", "Unknown")
        # Surface the most clinically actionable classification
        priority = {"Pathogenic": 4, "Likely Pathogenic": 3, "Drug Response": 2, "VUS": 1, "Likely Benign": 0, "Benign": 0}
        chosen = sig1 if priority.get(sig1, 0) >= priority.get(sig2, 0) else sig2
        return {
            "gene": gene,
            "diplotype": result["diplotype"],
            "phenotype": result["predicted_phenotype"],
            "clinvar_classification": chosen,
            "allele1_significance": sig1,
            "allele2_significance": sig2,
            "allele1_id": result["allele1"].get("id"),
            "allele2_id": result["allele2"].get("id"),
        }

    # Single allele only (treat as heterozygous with *1 reference)
    result = classify_diplotype(gene, allele1, "*1")
    return {
        "gene": gene,
        "diplotype": f"{allele1}/*1 (assumed)",
        "phenotype": result["predicted_phenotype"],
        "clinvar_classification": result["allele1"].get("clinical_significance", "Unknown"),
        "note": "Second allele not specified — assumed wild-type (*1)",
    }


# ── Main tool ─────────────────────────────────────────────────────────────────

def review_medications_pgx(
    medications: str,
    pgx_variants: str,
    tool_context: ToolContext,
) -> dict:
    """
    Reviews medications against the patient's pharmacogenomic profile for drug-gene interactions.

    Args:
        medications: Comma-separated list of current medications
            (e.g. 'Codeine 30mg, Enoxaparin 40mg, Ondansetron 4mg').
        pgx_variants: Known pharmacogenomic variants for this patient
            (e.g. 'CYP2D6 *4/*4, CYP2C19 *1/*1, VKORC1 AG') or 'unknown' if not available.

    Returns structured flags with risk levels, CPIC-guided recommendations,
    ClinVar classifications, and alternative drug suggestions.
    """
    patient_id = tool_context.state.get("patient_id", "unknown")
    logger.info(
        "tool_review_medications_pgx patient_id=%s medications=%s variants=%s",
        patient_id, medications, pgx_variants,
    )

    parsed_variants = _parse_pgx_variants(pgx_variants)
    parsed_meds = _parse_medications(medications)

    # Build the patient's PGx profile
    pgx_profile: dict[str, dict] = {}
    for variant in parsed_variants:
        resolved = _resolve_phenotype(variant)
        pgx_profile[resolved["gene"]] = resolved

    # If we have no PGx data, return informational response
    if not pgx_profile:
        return {
            "status": "no_pgx_data",
            "patient_id": patient_id,
            "message": (
                "No pharmacogenomic variant data available for this patient. "
                "Cannot perform drug-gene interaction analysis without genomic profile. "
                "Recommend ordering a PGx panel covering CYP2D6, CYP2C19, CYP2C9, VKORC1, DPYD "
                "before high-risk medication decisions."
            ),
            "medications_reviewed": parsed_meds,
            "actionable_genes_for_post_op_care": [
                "CYP2D6 (codeine, tramadol, oxycodone, ondansetron)",
                "CYP2C19 (clopidogrel)",
                "CYP2C9 + VKORC1 (warfarin, celecoxib, ibuprofen)",
                "DPYD (fluoropyrimidines)",
            ],
        }

    # Check each medication against the PGx profile
    medication_flags: list[dict] = []
    medications_cleared: list[dict] = []

    for med_string in parsed_meds:
        drug_name = _extract_drug_name(med_string)
        pairs = find_drug_gene_pair(drug_name)

        if not pairs:
            medications_cleared.append({
                "medication": med_string,
                "status": "No CPIC-listed drug-gene interaction for this medication.",
            })
            continue

        flagged_for_this_med = False
        for pair in pairs:
            primary_gene = pair["gene"]
            secondary_gene = pair.get("secondary_gene")

            # Check primary gene
            if primary_gene in pgx_profile:
                phenotype = pgx_profile[primary_gene]["phenotype"]
                interaction = check_interaction(drug_name, primary_gene, phenotype)
                if interaction and interaction.get("risk_level", "NONE") not in ("NONE",):
                    medication_flags.append({
                        "medication": med_string,
                        "drug": interaction["drug"],
                        "gene": primary_gene,
                        "patient_phenotype": phenotype,
                        "patient_diplotype": pgx_profile[primary_gene].get("diplotype"),
                        "risk_level": interaction["risk_level"],
                        "clinical_effect": interaction["clinical_effect"],
                        "recommendation": interaction["recommendation"],
                        "mechanism": interaction.get("mechanism"),
                        "cpic_strength": interaction.get("cpic_strength"),
                        "evidence": {
                            "cpic": interaction.get("cpic_citation"),
                            "cpic_url": interaction.get("cpic_url"),
                            "clinvar_classification": pgx_profile[primary_gene].get("clinvar_classification"),
                        },
                    })
                    flagged_for_this_med = True

            # Check secondary gene (e.g. VKORC1 for warfarin)
            if secondary_gene and secondary_gene in pgx_profile:
                phenotype2 = pgx_profile[secondary_gene]["phenotype"]
                interaction2 = check_interaction(drug_name, secondary_gene, phenotype2)
                if interaction2 and interaction2.get("risk_level", "NONE") not in ("NONE",):
                    medication_flags.append({
                        "medication": med_string,
                        "drug": interaction2["drug"],
                        "gene": secondary_gene,
                        "patient_phenotype": phenotype2,
                        "patient_diplotype": pgx_profile[secondary_gene].get("diplotype"),
                        "risk_level": interaction2["risk_level"],
                        "clinical_effect": interaction2["clinical_effect"],
                        "recommendation": interaction2["recommendation"],
                        "cpic_strength": interaction2.get("cpic_strength"),
                        "evidence": {
                            "cpic": interaction2.get("cpic_citation"),
                            "cpic_url": interaction2.get("cpic_url"),
                            "clinvar_classification": pgx_profile[secondary_gene].get("clinvar_classification"),
                        },
                    })
                    flagged_for_this_med = True

        if not flagged_for_this_med:
            medications_cleared.append({
                "medication": med_string,
                "status": (
                    f"CPIC drug-gene pair exists but patient phenotype carries no "
                    f"actionable risk for {drug_name} at standard dosing."
                ),
            })

    # Determine overall risk
    risk_priority = {"HIGH": 3, "MODERATE": 2, "LOW": 1, "NONE": 0}
    overall_risk = "NONE"
    for flag in medication_flags:
        if risk_priority.get(flag["risk_level"], 0) > risk_priority.get(overall_risk, 0):
            overall_risk = flag["risk_level"]

    return {
        "status": "success",
        "patient_id": patient_id,
        "patient_pgx_profile": pgx_profile,
        "medications_reviewed": parsed_meds,
        "medication_flags": medication_flags,
        "medications_cleared": medications_cleared,
        "overall_risk_level": overall_risk,
        "summary": {
            "total_medications": len(parsed_meds),
            "flagged_count": len(medication_flags),
            "cleared_count": len(medications_cleared),
            "genes_analyzed": list(pgx_profile.keys()),
        },
    }
