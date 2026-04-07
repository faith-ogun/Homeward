"""
Drug-gene interaction lookup tables.

Sourced from CPIC (Clinical Pharmacogenetics Implementation Consortium)
guidelines. These are curated, evidence-based pairs — NOT LLM-generated.

Each entry maps a drug to the gene(s) involved, the clinical consequence
by phenotype, and the CPIC recommendation.

Reference: https://cpicpgx.org/guidelines/
"""

# ── Phenotype definitions ──────────────────────────────────────────────────────

# Standard phenotype categories used by CPIC:
#   "Poor Metabolizer" (PM)
#   "Intermediate Metabolizer" (IM)
#   "Normal Metabolizer" (NM)        — also called "Extensive Metabolizer" in older literature
#   "Rapid Metabolizer" (RM)
#   "Ultrarapid Metabolizer" (UM)

# For VKORC1 (warfarin sensitivity):
#   "High Sensitivity"               — AA genotype at -1639G>A
#   "Intermediate Sensitivity"       — AG genotype
#   "Normal Sensitivity"             — GG genotype

# ── Drug-Gene Interaction Table ────────────────────────────────────────────────

DRUG_GENE_PAIRS: list[dict] = [

    # ── Codeine ↔ CYP2D6 ────────────────────────────────────────────────────
    {
        "drug": "Codeine",
        "drug_aliases": ["codeine", "codeine phosphate", "codeine sulfate"],
        "gene": "CYP2D6",
        "category": "Opioid Analgesic",
        "mechanism": (
            "Codeine is a prodrug that requires CYP2D6-mediated O-demethylation "
            "to morphine for analgesic effect. The extent of conversion directly "
            "determines clinical response."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Greatly reduced morphine formation. Patient will experience "
                    "significantly reduced or no analgesic effect from codeine."
                ),
                "recommendation": (
                    "Avoid codeine. Use an alternative analgesic NOT metabolised by "
                    "CYP2D6: morphine, oxymorphone, non-opioid alternatives "
                    "(acetaminophen, NSAIDs, ketorolac), or a non-codeine opioid."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": (
                    "Reduced morphine formation. Patient may experience diminished "
                    "analgesic response at standard doses."
                ),
                "recommendation": (
                    "Use codeine with caution and monitor for adequate pain relief. "
                    "If insufficient analgesia, switch to an alternative not dependent "
                    "on CYP2D6 activation."
                ),
                "cpic_strength": "Moderate",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal analgesic response.",
                "recommendation": "Use codeine per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Ultrarapid Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Markedly increased morphine formation. Risk of respiratory "
                    "depression, sedation, and potentially fatal toxicity, even "
                    "at standard doses."
                ),
                "recommendation": (
                    "Avoid codeine. Use an alternative analgesic NOT metabolised by "
                    "CYP2D6. If opioid is required, use morphine or oxymorphone at "
                    "reduced doses with close monitoring."
                ),
                "cpic_strength": "Strong",
            },
        },
        "cpic_citation": "CPIC Guideline for CYP2D6 and Codeine Therapy (Crews et al., 2021)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-codeine-therapy/",
    },

    # ── Tramadol ↔ CYP2D6 ───────────────────────────────────────────────────
    {
        "drug": "Tramadol",
        "drug_aliases": ["tramadol", "tramadol hydrochloride", "ultram"],
        "gene": "CYP2D6",
        "category": "Opioid Analgesic",
        "mechanism": (
            "Tramadol is a prodrug. CYP2D6 converts tramadol to its active "
            "metabolite O-desmethyltramadol (M1), which has ~200x greater "
            "affinity for the mu-opioid receptor."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Significantly reduced formation of active metabolite M1. "
                    "Diminished analgesic effect."
                ),
                "recommendation": (
                    "Avoid tramadol. Use an alternative analgesic not dependent "
                    "on CYP2D6 activation."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": "Reduced M1 formation. May have diminished response.",
                "recommendation": "Monitor for adequate pain relief. Consider alternatives if insufficient.",
                "cpic_strength": "Moderate",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal analgesic response.",
                "recommendation": "Use tramadol per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Ultrarapid Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Increased M1 formation. Risk of respiratory depression and "
                    "toxicity, similar to codeine."
                ),
                "recommendation": "Avoid tramadol. Use an alternative analgesic.",
                "cpic_strength": "Strong",
            },
        },
        "cpic_citation": "CPIC Guideline for CYP2D6 and Tramadol Therapy (2024 Update)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-codeine-and-tramadol-therapy/",
    },

    # ── Oxycodone ↔ CYP2D6 ──────────────────────────────────────────────────
    {
        "drug": "Oxycodone",
        "drug_aliases": ["oxycodone", "oxycodone hydrochloride", "oxycontin", "percocet"],
        "gene": "CYP2D6",
        "category": "Opioid Analgesic",
        "mechanism": (
            "Oxycodone is partially metabolised by CYP2D6 to oxymorphone (active). "
            "However, oxycodone itself has analgesic activity via the parent compound "
            "and CYP3A4-mediated pathways, making it less dependent on CYP2D6 than "
            "codeine or tramadol."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "LOW",
                "clinical_effect": (
                    "Reduced oxymorphone formation, but parent compound retains "
                    "analgesic activity. Clinical impact is less pronounced than "
                    "with codeine/tramadol."
                ),
                "recommendation": (
                    "Use oxycodone with awareness of potentially reduced efficacy. "
                    "Monitor pain control and adjust dose if needed."
                ),
                "cpic_strength": "Optional",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal analgesic response.",
                "recommendation": "Use oxycodone per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Ultrarapid Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": (
                    "Increased oxymorphone formation. Possible increased opioid "
                    "effect and risk of adverse reactions."
                ),
                "recommendation": "Use with caution. Consider lower starting dose and monitor.",
                "cpic_strength": "Optional",
            },
        },
        "cpic_citation": "CPIC Guideline for CYP2D6 and Opioid Therapy",
        "cpic_url": "https://cpicpgx.org/guidelines/",
    },

    # ── Celecoxib ↔ CYP2C9 ──────────────────────────────────────────────────
    {
        "drug": "Celecoxib",
        "drug_aliases": ["celecoxib", "celebrex"],
        "gene": "CYP2C9",
        "category": "NSAID (COX-2 Inhibitor)",
        "mechanism": (
            "Celecoxib is primarily metabolised by CYP2C9. Reduced CYP2C9 "
            "activity leads to increased celecoxib exposure (higher plasma "
            "concentrations for longer), increasing the risk of GI and "
            "cardiovascular adverse effects."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Significantly increased celecoxib exposure (~3-7 fold). "
                    "Increased risk of GI bleeding, cardiovascular events, "
                    "and renal toxicity."
                ),
                "recommendation": (
                    "Use the lowest effective dose (reduce by 50% or more) or "
                    "consider an alternative NSAID less dependent on CYP2C9 "
                    "(e.g. naproxen, though it also has CYP2C9 involvement, "
                    "or acetaminophen for non-inflammatory pain)."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": "Moderately increased celecoxib exposure (~2-3 fold).",
                "recommendation": "Reduce dose by 50% or use the lowest effective dose.",
                "cpic_strength": "Strong",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal metabolism and drug exposure.",
                "recommendation": "Use celecoxib per standard prescribing.",
                "cpic_strength": "Strong",
            },
        },
        "cpic_citation": "CPIC Guideline for NSAIDs and CYP2C9 (Theken et al., 2020)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-nsaids-based-on-cyp2c9-genotype/",
    },

    # ── Ibuprofen ↔ CYP2C9 ──────────────────────────────────────────────────
    {
        "drug": "Ibuprofen",
        "drug_aliases": ["ibuprofen", "advil", "motrin", "nurofen", "brufen"],
        "gene": "CYP2C9",
        "category": "NSAID",
        "mechanism": (
            "Ibuprofen is metabolised by CYP2C9. Reduced activity leads to "
            "increased drug exposure, raising the risk of GI bleeding and "
            "renal adverse effects."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": "Increased ibuprofen exposure. Higher risk of GI and renal side effects.",
                "recommendation": (
                    "Use the lowest effective dose for the shortest duration. "
                    "Consider acetaminophen as an alternative for non-inflammatory pain."
                ),
                "cpic_strength": "Moderate",
            },
            "Intermediate Metabolizer": {
                "risk_level": "LOW",
                "clinical_effect": "Mildly increased exposure. Generally well-tolerated at standard doses.",
                "recommendation": "Use with standard monitoring. Prefer lowest effective dose.",
                "cpic_strength": "Optional",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal metabolism.",
                "recommendation": "Use ibuprofen per standard prescribing.",
                "cpic_strength": "Strong",
            },
        },
        "cpic_citation": "CPIC Guideline for NSAIDs and CYP2C9 (Theken et al., 2020)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-nsaids-based-on-cyp2c9-genotype/",
    },

    # ── Warfarin ↔ CYP2C9 + VKORC1 ──────────────────────────────────────────
    {
        "drug": "Warfarin",
        "drug_aliases": ["warfarin", "coumadin", "jantoven"],
        "gene": "CYP2C9",
        "secondary_gene": "VKORC1",
        "category": "Anticoagulant",
        "mechanism": (
            "Warfarin is metabolised by CYP2C9 (S-warfarin, the more active enantiomer). "
            "VKORC1 is warfarin's drug target — variants in the VKORC1 promoter (-1639G>A) "
            "reduce VKORC1 expression, making patients more sensitive to warfarin's effect. "
            "CYP2C9 and VKORC1 genotypes together explain ~40% of warfarin dose variability."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Significantly reduced warfarin clearance. Higher drug levels lead to "
                    "increased risk of over-anticoagulation and bleeding, especially during "
                    "initiation. Combined with VKORC1 sensitivity, bleeding risk is substantial."
                ),
                "recommendation": (
                    "Reduce initial warfarin dose by 50-80% compared to standard. "
                    "Use pharmacogenomic dosing algorithms (e.g. IWPC or Gage) to calculate "
                    "personalised dose. Monitor INR frequently during initiation."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": "Reduced warfarin clearance. Moderately increased bleeding risk at standard doses.",
                "recommendation": (
                    "Reduce initial dose by 20-40%. Monitor INR closely. "
                    "Consider pharmacogenomic dosing algorithm."
                ),
                "cpic_strength": "Strong",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal warfarin metabolism.",
                "recommendation": "Standard dosing with routine INR monitoring.",
                "cpic_strength": "Strong",
            },
        },
        "vkorc1_interactions": {
            "High Sensitivity": {
                "genotype": "AA (-1639G>A)",
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Reduced VKORC1 expression. Patient requires significantly lower "
                    "warfarin doses (typically 1-2 mg/day vs standard 5 mg/day)."
                ),
                "recommendation": "Reduce dose significantly. Use PGx dosing algorithm.",
            },
            "Intermediate Sensitivity": {
                "genotype": "AG (-1639G>A)",
                "risk_level": "MODERATE",
                "clinical_effect": "Moderately reduced VKORC1 expression. Requires lower-than-average dose.",
                "recommendation": "Reduce dose moderately. Monitor INR closely during initiation.",
            },
            "Normal Sensitivity": {
                "genotype": "GG (-1639G>A)",
                "risk_level": "NONE",
                "clinical_effect": "Normal VKORC1 expression. Standard warfarin sensitivity.",
                "recommendation": "Standard dosing.",
            },
        },
        "cpic_citation": "CPIC Guideline for Pharmacogenetics-Guided Warfarin Dosing (Johnson et al., 2017)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-warfarin-based-on-cyp2c9-and-vkorc1-genotype/",
    },

    # ── Clopidogrel ↔ CYP2C19 ───────────────────────────────────────────────
    {
        "drug": "Clopidogrel",
        "drug_aliases": ["clopidogrel", "plavix"],
        "gene": "CYP2C19",
        "category": "Antiplatelet Agent",
        "mechanism": (
            "Clopidogrel is a prodrug that requires CYP2C19-mediated activation "
            "to its active thiol metabolite. Without adequate CYP2C19 activity, "
            "the drug cannot inhibit platelet aggregation effectively."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Significantly reduced active metabolite formation. Markedly "
                    "diminished antiplatelet effect. Increased risk of cardiovascular "
                    "events (stent thrombosis, stroke, MI)."
                ),
                "recommendation": (
                    "Use an alternative antiplatelet agent not dependent on CYP2C19: "
                    "prasugrel or ticagrelor (if no contraindications)."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "MODERATE",
                "clinical_effect": "Reduced active metabolite. Diminished antiplatelet response.",
                "recommendation": (
                    "Consider alternative antiplatelet (prasugrel, ticagrelor). "
                    "If clopidogrel must be used, consider higher maintenance dose "
                    "with platelet function testing."
                ),
                "cpic_strength": "Moderate",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal antiplatelet response.",
                "recommendation": "Use clopidogrel per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Rapid Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Normal to increased active metabolite. Adequate antiplatelet effect.",
                "recommendation": "Use clopidogrel per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Ultrarapid Metabolizer": {
                "risk_level": "LOW",
                "clinical_effect": "Increased active metabolite. May have increased bleeding risk.",
                "recommendation": "Use clopidogrel per standard prescribing. Monitor for bleeding.",
                "cpic_strength": "Optional",
            },
        },
        "cpic_citation": "CPIC Guideline for CYP2C19 and Clopidogrel Therapy (Lee et al., 2022)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-clopidogrel-therapy/",
    },

    # ── Ondansetron ↔ CYP2D6 ────────────────────────────────────────────────
    {
        "drug": "Ondansetron",
        "drug_aliases": ["ondansetron", "zofran"],
        "gene": "CYP2D6",
        "category": "Antiemetic (5-HT3 Antagonist)",
        "mechanism": (
            "Ondansetron is partially metabolised by CYP2D6. While CYP2D6 status "
            "can affect drug levels, the clinical impact is generally modest at "
            "standard antiemetic doses used post-operatively."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "LOW",
                "clinical_effect": (
                    "Increased ondansetron exposure. May have slightly enhanced "
                    "antiemetic effect. Risk of QT prolongation at high doses."
                ),
                "recommendation": "Use standard dose. Avoid high doses. Monitor for QT prolongation if other risk factors.",
                "cpic_strength": "Optional",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal response.",
                "recommendation": "Use ondansetron per standard prescribing.",
                "cpic_strength": "Strong",
            },
            "Ultrarapid Metabolizer": {
                "risk_level": "LOW",
                "clinical_effect": "Reduced ondansetron exposure. May have slightly diminished antiemetic effect.",
                "recommendation": (
                    "If antiemetic effect is insufficient, consider an alternative "
                    "antiemetic (granisetron, which is not CYP2D6 dependent)."
                ),
                "cpic_strength": "Optional",
            },
        },
        "cpic_citation": "CPIC Guideline for CYP2D6 and Ondansetron/Tropisetron Therapy",
        "cpic_url": "https://cpicpgx.org/guidelines/",
    },

    # ── Fluorouracil (5-FU) ↔ DPYD ──────────────────────────────────────────
    {
        "drug": "Fluorouracil",
        "drug_aliases": ["fluorouracil", "5-FU", "5-fluorouracil", "adrucil", "capecitabine"],
        "gene": "DPYD",
        "category": "Chemotherapy (Antimetabolite)",
        "mechanism": (
            "Dihydropyrimidine dehydrogenase (DPD, encoded by DPYD) is the "
            "rate-limiting enzyme in fluoropyrimidine catabolism. Reduced DPD "
            "activity leads to accumulation of 5-FU, causing severe and "
            "potentially fatal toxicity."
        ),
        "interactions_by_phenotype": {
            "Poor Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Complete or near-complete DPD deficiency. Risk of severe, "
                    "life-threatening toxicity: neutropenia, mucositis, "
                    "hand-foot syndrome, diarrhoea, and death."
                ),
                "recommendation": (
                    "Avoid fluoropyrimidines entirely. Use alternative "
                    "chemotherapy regimen."
                ),
                "cpic_strength": "Strong",
            },
            "Intermediate Metabolizer": {
                "risk_level": "HIGH",
                "clinical_effect": (
                    "Partial DPD deficiency. Significantly increased risk of "
                    "severe toxicity at standard doses."
                ),
                "recommendation": (
                    "Reduce dose by 50% with dose titration based on tolerance, "
                    "or use an alternative regimen."
                ),
                "cpic_strength": "Strong",
            },
            "Normal Metabolizer": {
                "risk_level": "NONE",
                "clinical_effect": "Expected normal metabolism of fluoropyrimidines.",
                "recommendation": "Use standard dosing with routine toxicity monitoring.",
                "cpic_strength": "Strong",
            },
        },
        "cpic_citation": "CPIC Guideline for Fluoropyrimidines and DPYD (Amstutz et al., 2018)",
        "cpic_url": "https://cpicpgx.org/guidelines/cpic-guideline-for-fluoropyrimidines-and-dpyd/",
    },
]


# ── Lookup helpers ─────────────────────────────────────────────────────────────

def find_drug_gene_pair(drug_name: str) -> list[dict]:
    """
    Find all drug-gene interaction entries for a given drug name.
    Case-insensitive. Returns a list (may be empty).
    """
    drug_lower = drug_name.strip().lower()
    results = []
    for pair in DRUG_GENE_PAIRS:
        if drug_lower == pair["drug"].lower():
            results.append(pair)
            continue
        for alias in pair["drug_aliases"]:
            if drug_lower in alias.lower() or alias.lower() in drug_lower:
                results.append(pair)
                break
    return results


def check_interaction(drug_name: str, gene: str, phenotype: str) -> dict | None:
    """
    Check if a specific drug-gene-phenotype combination has a known interaction.

    Returns the interaction dict (risk_level, clinical_effect, recommendation)
    or None if no interaction is found.
    """
    pairs = find_drug_gene_pair(drug_name)
    gene_upper = gene.strip().upper()
    phenotype_title = phenotype.strip().title()

    for pair in pairs:
        if pair["gene"].upper() == gene_upper:
            interaction = pair["interactions_by_phenotype"].get(phenotype_title)
            if interaction:
                return {
                    "drug": pair["drug"],
                    "gene": pair["gene"],
                    "phenotype": phenotype_title,
                    "category": pair["category"],
                    "mechanism": pair["mechanism"],
                    **interaction,
                    "cpic_citation": pair["cpic_citation"],
                    "cpic_url": pair["cpic_url"],
                }

        # Check secondary gene (e.g. VKORC1 for warfarin)
        if pair.get("secondary_gene", "").upper() == gene_upper:
            vkorc1_data = pair.get("vkorc1_interactions", {}).get(phenotype_title)
            if vkorc1_data:
                return {
                    "drug": pair["drug"],
                    "gene": pair.get("secondary_gene"),
                    "phenotype": phenotype_title,
                    "category": pair["category"],
                    **vkorc1_data,
                    "cpic_citation": pair["cpic_citation"],
                    "cpic_url": pair["cpic_url"],
                }

    return None


def get_all_flagged_genes() -> list[str]:
    """Return a sorted list of all genes that have drug interactions in this table."""
    genes = set()
    for pair in DRUG_GENE_PAIRS:
        genes.add(pair["gene"])
        if pair.get("secondary_gene"):
            genes.add(pair["secondary_gene"])
    return sorted(genes)
