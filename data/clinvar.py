"""
Pre-cached ClinVar variant classifications for common PGx star alleles.

Source: https://www.ncbi.nlm.nih.gov/clinvar/

This is a local lookup — no real-time API calls to ClinVar. Entries cover
the ~50 most common PGx star alleles relevant to post-surgical medications.

Each entry maps a variant identifier (star allele or rsID) to:
  - clinical_significance: Pathogenic / Likely Pathogenic / VUS / Likely Benign / Benign / Drug Response
  - clinvar_variation_id: ClinVar accession for citation
  - review_status: e.g. "reviewed by expert panel", "criteria provided, multiple submitters"
  - description: brief plain-language summary
"""

CLINVAR_VARIANTS: dict[str, dict] = {

    # ── CYP2D6 Star Alleles ──────────────────────────────────────────────────

    "CYP2D6*1": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*1 (wild-type / reference)",
        "function": "Normal Function",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "N/A — reference allele",
        "review_status": "N/A",
        "description": "Wild-type allele. Normal CYP2D6 enzyme activity.",
    },
    "CYP2D6*2": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*2",
        "function": "Normal Function",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "N/A",
        "review_status": "Practice guideline",
        "description": "Common variant with normal enzyme activity. No clinical action needed.",
    },
    "CYP2D6*3": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*3 (2549delA)",
        "rsid": "rs35742686",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018065",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Frameshift variant causing non-functional CYP2D6 enzyme. "
            "One of the most common non-functional alleles in European populations."
        ),
    },
    "CYP2D6*4": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*4 (1846G>A, splicing defect)",
        "rsid": "rs3892097",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018068",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Most common non-functional CYP2D6 allele worldwide. Splicing defect "
            "abolishes enzyme activity. Allele frequency ~12-21% in European "
            "populations. Homozygous *4/*4 = Poor Metabolizer."
        ),
    },
    "CYP2D6*5": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*5 (gene deletion)",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018069",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Complete gene deletion. No CYP2D6 protein produced. "
            "Found across all populations at 2-7% frequency."
        ),
    },
    "CYP2D6*6": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*6 (1707delT)",
        "rsid": "rs5030655",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018070",
        "review_status": "Reviewed by expert panel",
        "description": "Frameshift variant causing non-functional enzyme. Less common than *4 or *5.",
    },
    "CYP2D6*9": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*9 (2615_2617delAAG)",
        "rsid": "rs5030656",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018073",
        "review_status": "Reviewed by expert panel",
        "description": "In-frame deletion resulting in decreased but not absent enzyme activity.",
    },
    "CYP2D6*10": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*10 (100C>T, Pro34Ser)",
        "rsid": "rs1065852",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018074",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Unstable enzyme with decreased activity. Most common decreased-function "
            "allele in East Asian populations (~40-70% frequency)."
        ),
    },
    "CYP2D6*17": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*17 (1023C>T, Thr107Ile)",
        "rsid": "rs28371706",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018078",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Decreased enzyme activity. Most common decreased-function "
            "allele in African populations (~20-35% frequency)."
        ),
    },
    "CYP2D6*41": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6*41 (2988G>A, splicing)",
        "rsid": "rs28371725",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018088",
        "review_status": "Reviewed by expert panel",
        "description": "Decreased enzyme activity due to aberrant splicing. Common in Middle Eastern populations.",
    },
    "CYP2D6*xN": {
        "gene": "CYP2D6",
        "common_name": "CYP2D6 gene duplication/multiplication",
        "function": "Increased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "N/A — structural variant",
        "review_status": "Practice guideline",
        "description": (
            "Gene duplication or multiplication resulting in >2 functional copies. "
            "Leads to ultrarapid metabolizer phenotype. Found in 1-10% of "
            "populations, highest in East African and Oceanian populations."
        ),
    },

    # ── CYP2C19 Star Alleles ─────────────────────────────────────────────────

    "CYP2C19*1": {
        "gene": "CYP2C19",
        "common_name": "CYP2C19*1 (wild-type / reference)",
        "function": "Normal Function",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "N/A — reference allele",
        "review_status": "N/A",
        "description": "Wild-type allele. Normal CYP2C19 enzyme activity.",
    },
    "CYP2C19*2": {
        "gene": "CYP2C19",
        "common_name": "CYP2C19*2 (681G>A, splicing defect)",
        "rsid": "rs4244285",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000016897",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Most common loss-of-function CYP2C19 allele. Splicing defect "
            "abolishes activity. ~15% in Europeans, ~30% in East Asians."
        ),
    },
    "CYP2C19*3": {
        "gene": "CYP2C19",
        "common_name": "CYP2C19*3 (636G>A, premature stop)",
        "rsid": "rs4986893",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000016898",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Premature stop codon. Non-functional allele. Rare in Europeans "
            "(~0.04%), more common in East Asians (~5-8%)."
        ),
    },
    "CYP2C19*17": {
        "gene": "CYP2C19",
        "common_name": "CYP2C19*17 (-806C>T, increased transcription)",
        "rsid": "rs12248560",
        "function": "Increased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000016900",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Promoter variant increasing CYP2C19 transcription. Results in "
            "rapid or ultrarapid metabolizer phenotype. ~21% in Europeans."
        ),
    },

    # ── CYP2C9 Star Alleles ──────────────────────────────────────────────────

    "CYP2C9*1": {
        "gene": "CYP2C9",
        "common_name": "CYP2C9*1 (wild-type / reference)",
        "function": "Normal Function",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "N/A — reference allele",
        "review_status": "N/A",
        "description": "Wild-type allele. Normal CYP2C9 enzyme activity.",
    },
    "CYP2C9*2": {
        "gene": "CYP2C9",
        "common_name": "CYP2C9*2 (430C>T, Arg144Cys)",
        "rsid": "rs1799853",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018063",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Decreased enzyme activity (~30-50% of wild-type). "
            "~13% frequency in Europeans. Affects warfarin, celecoxib, and NSAID dosing."
        ),
    },
    "CYP2C9*3": {
        "gene": "CYP2C9",
        "common_name": "CYP2C9*3 (1075A>C, Ile359Leu)",
        "rsid": "rs1057910",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018064",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Markedly decreased enzyme activity (~10-20% of wild-type). "
            "~7% in Europeans. Strong impact on warfarin dose requirements. "
            "*2/*3 or *3/*3 = Poor Metabolizer."
        ),
    },

    # ── VKORC1 ───────────────────────────────────────────────────────────────

    "VKORC1 -1639G>A (GG)": {
        "gene": "VKORC1",
        "common_name": "VKORC1 -1639G>A GG genotype",
        "rsid": "rs9923231",
        "function": "Normal Expression",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "VCV000016901",
        "review_status": "Reviewed by expert panel",
        "description": "Normal VKORC1 expression. Standard warfarin sensitivity.",
    },
    "VKORC1 -1639G>A (AG)": {
        "gene": "VKORC1",
        "common_name": "VKORC1 -1639G>A AG genotype",
        "rsid": "rs9923231",
        "function": "Decreased Expression",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000016901",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Heterozygous. Intermediate VKORC1 expression. Increased warfarin "
            "sensitivity — requires lower dose than GG genotype."
        ),
    },
    "VKORC1 -1639G>A (AA)": {
        "gene": "VKORC1",
        "common_name": "VKORC1 -1639G>A AA genotype",
        "rsid": "rs9923231",
        "function": "Low Expression",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000016901",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Homozygous variant. Low VKORC1 expression. High warfarin sensitivity — "
            "typically requires 50-70% dose reduction. ~14% in Europeans, ~90% in East Asians."
        ),
    },

    # ── DPYD Star Alleles ────────────────────────────────────────────────────

    "DPYD*1": {
        "gene": "DPYD",
        "common_name": "DPYD*1 (wild-type / reference)",
        "function": "Normal Function",
        "clinical_significance": "Benign",
        "clinvar_variation_id": "N/A — reference allele",
        "review_status": "N/A",
        "description": "Wild-type allele. Normal DPD enzyme activity.",
    },
    "DPYD*2A": {
        "gene": "DPYD",
        "common_name": "DPYD*2A (IVS14+1G>A, splice site)",
        "rsid": "rs3918290",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018100",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Splice site variant abolishing DPD activity. Most clinically "
            "significant DPYD variant. ~1-2% in Europeans. Homozygous = "
            "complete DPD deficiency with risk of fatal fluoropyrimidine toxicity."
        ),
    },
    "DPYD c.2846A>T": {
        "gene": "DPYD",
        "common_name": "DPYD c.2846A>T (D949V)",
        "rsid": "rs67376798",
        "function": "Decreased Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018101",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Decreased DPD activity. ~1% in Europeans. Carriers require "
            "fluoropyrimidine dose reduction."
        ),
    },
    "DPYD c.1679T>G": {
        "gene": "DPYD",
        "common_name": "DPYD c.1679T>G (DPYD*13)",
        "rsid": "rs55886062",
        "function": "No Function",
        "clinical_significance": "Pathogenic",
        "clinvar_variation_id": "VCV000018102",
        "review_status": "Reviewed by expert panel",
        "description": "Non-functional allele. Rare but clinically significant.",
    },
    "DPYD c.1236G>A": {
        "gene": "DPYD",
        "common_name": "DPYD c.1236G>A (HapB3)",
        "rsid": "rs56038477",
        "function": "Decreased Function",
        "clinical_significance": "Drug Response",
        "clinvar_variation_id": "VCV000018103",
        "review_status": "Reviewed by expert panel",
        "description": (
            "Decreased DPD activity via aberrant splicing. ~4-5% in Europeans. "
            "Dose reduction recommended for fluoropyrimidines."
        ),
    },
}


# ── Lookup helpers ─────────────────────────────────────────────────────────────

def get_variant_classification(variant_id: str) -> dict | None:
    """
    Look up ClinVar classification for a variant.
    Accepts star allele notation (e.g. 'CYP2D6*4') or rsID.
    Returns the variant dict or None.
    """
    # Direct key match
    if variant_id in CLINVAR_VARIANTS:
        return CLINVAR_VARIANTS[variant_id]

    # Search by rsID
    variant_lower = variant_id.strip().lower()
    for key, data in CLINVAR_VARIANTS.items():
        if data.get("rsid", "").lower() == variant_lower:
            return data

    return None


def classify_diplotype(gene: str, allele1: str, allele2: str) -> dict:
    """
    Classify a diplotype (pair of alleles) for a gene.

    Args:
        gene: Gene name (e.g. 'CYP2D6')
        allele1: First allele (e.g. '*4')
        allele2: Second allele (e.g. '*4')

    Returns dict with diplotype, phenotype, and classification details.
    """
    full_allele1 = f"{gene}{allele1}" if not allele1.startswith(gene) else allele1
    full_allele2 = f"{gene}{allele2}" if not allele2.startswith(gene) else allele2

    data1 = get_variant_classification(full_allele1)
    data2 = get_variant_classification(full_allele2)

    # Determine phenotype based on function of each allele
    functions = []
    for data in [data1, data2]:
        if data:
            functions.append(data.get("function", "Unknown"))
        else:
            functions.append("Unknown")

    phenotype = _determine_phenotype(gene, functions)

    return {
        "gene": gene,
        "diplotype": f"{allele1}/{allele2}",
        "allele1": {"id": full_allele1, **(data1 or {"clinical_significance": "Unknown"})},
        "allele2": {"id": full_allele2, **(data2 or {"clinical_significance": "Unknown"})},
        "predicted_phenotype": phenotype,
    }


def _determine_phenotype(gene: str, functions: list[str]) -> str:
    """
    Determine metabolizer phenotype from two allele functions.
    Uses CPIC activity score approach (simplified).
    """
    score_map = {
        "Normal Function": 1.0,
        "Normal Expression": 1.0,
        "Decreased Function": 0.5,
        "Decreased Expression": 0.5,
        "No Function": 0.0,
        "Low Expression": 0.0,
        "Increased Function": 1.5,
    }

    scores = [score_map.get(f, 0.5) for f in functions]
    total = sum(scores)

    if gene in ("CYP2D6", "CYP2C19", "CYP2C9", "DPYD"):
        if total == 0:
            return "Poor Metabolizer"
        elif total <= 0.5:
            return "Poor Metabolizer"
        elif total <= 1.0:
            return "Intermediate Metabolizer"
        elif total <= 2.0:
            return "Normal Metabolizer"
        elif total <= 2.5:
            return "Rapid Metabolizer"
        else:
            return "Ultrarapid Metabolizer"

    return "Unknown"
