from app.config.constants import PRIMARY_GENE_MAP


CPIC_RULES = {

    "CODEINE": {
        "CYP2D6": {
            "PM": {
                "risk_label": "Ineffective",
                "severity": "high",
                "recommendation": "Avoid codeine. Use alternative analgesic not metabolized by CYP2D6."
            },
            "IM": {
                "risk_label": "Reduced Response",
                "severity": "moderate",
                "recommendation": "Consider alternative analgesic or monitor for reduced efficacy."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "UM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Avoid codeine due to risk of morphine toxicity."
            }
        }
    },

    "WARFARIN": {
        "CYP2C9": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Reduce initial dose significantly and monitor INR closely."
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
        },
        "VKORC1": {
            "High Sensitivity": {
                "risk_label": "Toxic",
                "severity": "high",
                "recommendation": "Lower initial dose due to increased warfarin sensitivity."
            },
            "Intermediate Sensitivity": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "recommendation": "Consider lower starting dose."
            },
            "Low Sensitivity": {
                "risk_label": "Reduced Response",
                "severity": "moderate",
                "recommendation": "May require higher dose to achieve therapeutic INR."
            }
        }
    },

    "CLOPIDOGREL": {
        "CYP2C19": {
            "PM": {
                "risk_label": "Ineffective",
                "severity": "critical",
                "recommendation": "Avoid clopidogrel. Use alternative antiplatelet (e.g., prasugrel or ticagrelor)."
            },
            "IM": {
                "risk_label": "Reduced Response",
                "severity": "high",
                "recommendation": "Consider alternative antiplatelet therapy."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "RM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Standard dosing appropriate."
            },
            "UM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Standard dosing appropriate."
            }
        }
    },

    "SIMVASTATIN": {
        "SLCO1B1": {
            "Normal": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "Decreased": {
                "risk_label": "Myopathy Risk",
                "severity": "moderate",
                "recommendation": "Use lower dose or consider alternative statin."
            },
            "Poor": {
                "risk_label": "Toxic",
                "severity": "high",
                "recommendation": "Avoid high doses. Consider alternative statin."
            }
        }
    },

    "AZATHIOPRINE": {
        "TPMT": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Avoid azathioprine or drastically reduce dose (≤10% of standard)."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "recommendation": "Reduce starting dose by 30–80% and monitor closely."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            }
        },
        "NUDT15": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Avoid azathioprine due to severe myelosuppression risk."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "recommendation": "Substantially reduce starting dose."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Standard dosing appropriate."
            }
        }
    },

    "FLUOROURACIL": {
        "DPYD": {
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "recommendation": "Reduce starting dose by 25–50% and titrate."
            },
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Avoid fluorouracil due to severe toxicity risk."
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
