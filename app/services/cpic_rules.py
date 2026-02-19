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
            "Normal Function": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "Decreased Function": {
                "risk_label": "Myopathy Risk",
                "severity": "moderate",
                "recommendation": "Use lower dose or consider alternative statin."
            },
            "Poor Function": {
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
            "Normal Metabolizer": {
                "risk_label": "Safe",
                "severity": "none",
                "recommendation": "Use standard dosing."
            },
            "Intermediate Metabolizer": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "recommendation": "Reduce starting dose by 25–50% and titrate."
            },
            "Poor Metabolizer": {
                "risk_label": "Toxic",
                "severity": "critical",
                "recommendation": "Avoid fluorouracil due to severe toxicity risk."
            }
        }
    }
}