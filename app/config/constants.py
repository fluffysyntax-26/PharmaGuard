SUPPORTED_DRUGS = {
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
}

PRIMARY_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

SUPPORTED_GENES = {
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
}

STAR_PHENOTYPE_MAP = {
    "CYP2D6": {
        "*1": "NM",
        "*2": "NM",
        "*3": "PM",
        "*4": "PM"
    },
    "CYP2C19": {
        "*1": "NM",
        "*2": "PM",
        "*3": "PM"
    },
    "CYP2C9": {
        "*1": "NM",
        "*2": "IM",
        "*3": "PM"
    },
    "SLCO1B1": {
        "*1": "Normal",
        "*5": "Decreased",
        "*15": "Poor"
    },
    "TPMT": {
        "*1": "NM",
        "*3A": "PM",
        "*3C": "IM"
    },
    "DPYD": {
        "*1": "NM",
        "*2A": "PM"
    }
}