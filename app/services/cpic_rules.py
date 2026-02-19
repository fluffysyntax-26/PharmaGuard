from app.config.constants import PRIMARY_GENE_MAP


CPIC_RULES = {

    "CODEINE": {
        "CYP2D6": {
            "PM": {
                "risk_label": "Ineffective",
                "severity": "high",
                "recommendation": "Avoid codeine. Consider alternative analgesic."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "recommendation": "Consider alternative analgesic or monitor response."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            }
        }
    },

    "WARFARIN": {
        "CYP2C9": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Significantly reduce initial dose and monitor INR closely."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "recommendation": "Lower starting dose and monitor INR."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Standard initial dosing."
            }
        }
    }
}

def evaluate_drug_risk(drug: str, profile: dict):

    drug = drug.upper()

    if drug not in PRIMARY_GENE_MAP:
        return unknown_response()

    gene = PRIMARY_GENE_MAP[drug]

    if gene not in profile:
        return unknown_response()

    phenotype = profile[gene]["phenotype"]

    gene_rules = CPIC_RULES.get(drug, {}).get(gene, {})

    if phenotype not in gene_rules:
        return unknown_response()

    rule = gene_rules[phenotype]

    return {
        "risk_label": rule["risk_label"],
        "severity": rule["severity"],
        "confidence_score": 1.0,
        "clinical_recommendation": {
            "guideline_source": "CPIC",
            "recommendation_summary": rule["recommendation"],
            "dose_adjustment": rule["recommendation"],
            "monitoring_advice": "Monitor patient response as per CPIC guidelines."
        }
    }

def unknown_response():
    return {
        "risk_label": "Unknown",
        "severity": "none",
        "confidence_score": 0.0,
        "clinical_recommendation": {
            "guideline_source": "CPIC",
            "recommendation_summary": "No actionable pharmacogenomic variant detected.",
            "dose_adjustment": "No specific adjustment recommended.",
            "monitoring_advice": "Follow standard clinical practice."
        }
    }
