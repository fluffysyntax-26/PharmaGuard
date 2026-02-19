from collections import defaultdict
from app.config.constants import STAR_PHENOTYPE_MAP, SUPPORTED_GENES


def build_profile(variants):
    """
    Build pharmacogenomic profile from detected variants.
    Automatically assumes *1 allele where no variant is detected.
    """

    gene_data = defaultdict(lambda: {
        "stars": [],
        "rsids": []
    })

    # Collect detected star alleles per gene
    for variant in variants:
        gene = variant["gene"]
        star = variant["star"]
        rsid = variant["rsid"]

        if gene not in SUPPORTED_GENES:
            continue

        gene_data[gene]["stars"].append(star)
        gene_data[gene]["rsids"].append(rsid)

    profile = {}

    # Ensure all supported genes are represented
    for gene in SUPPORTED_GENES:

        stars = gene_data[gene]["stars"]
        rsids = gene_data[gene]["rsids"]

        # If no variants detected → assume *1/*1
        if not stars:
            diplotype = "*1/*1"
            phenotype = resolve_phenotype(gene, ["*1", "*1"])

        # If single variant detected → assume *1 + variant
        elif len(stars) == 1:
            diplotype = f"*1/{stars[0]}"
            phenotype = resolve_phenotype(gene, ["*1", stars[0]])

        # If two variants detected → assume they represent two alleles
        else:
            diplotype = f"{stars[0]}/{stars[1]}"
            phenotype = resolve_phenotype(gene, stars[:2])

        profile[gene] = {
            "diplotype": diplotype,
            "phenotype": phenotype,
            "detected_variants": rsids
        }

    return profile


def resolve_phenotype(gene, stars):
    """
    Resolve phenotype from diplotype using simplified CPIC-consistent hierarchy.
    """

    mapping = STAR_PHENOTYPE_MAP.get(gene, {})

    phenotypes = [mapping.get(star, "NM") for star in stars]

    # --- CYP genes & TPMT & DPYD ---
    if gene in ["CYP2D6", "CYP2C19", "CYP2C9", "TPMT", "DPYD"]:

        # Two poor function alleles
        if phenotypes.count("PM") == 2:
            return "PM"

        # One poor allele OR one intermediate allele
        if "PM" in phenotypes or "IM" in phenotypes:
            return "IM"

        return "NM"

    # --- SLCO1B1 ---
    if gene == "SLCO1B1":

        if phenotypes.count("Poor") == 2:
            return "Poor Function"

        if "Poor" in phenotypes or "Decreased" in phenotypes:
            return "Decreased Function"

        return "Normal Function"

    # Fallback
    return "NM"