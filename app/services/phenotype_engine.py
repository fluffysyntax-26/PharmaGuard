from collections import defaultdict
from app.config.constants import STAR_PHENOTYPE_MAP

def build_profile(variants):
    gene_data = defaultdict(lambda: {
        "stars": [],
        "rsids": []
    })

    # Collect star alleles per gene
    for variant in variants:
        gene = variant["gene"]
        star = variant["star"]
        rsid = variant["rsid"]

        gene_data[gene]["stars"].append(star)
        gene_data[gene]["rsids"].append(rsid)

    profile = {}

    for gene, data in gene_data.items():
        stars = data["stars"]
        rsids = data["rsids"]

        # Build diplotype (simple approach)
        if len(stars) == 1:
            diplotype = f"{stars[0]}/{stars[0]}"
        else:
            diplotype = f"{stars[0]}/{stars[1]}"

        phenotype = resolve_phenotype(gene, stars)

        profile[gene] = {
            "diplotype": diplotype,
            "phenotype": phenotype,
            "detected_variants": rsids
        }

    return profile


def resolve_phenotype(gene, stars):
    mapping = STAR_PHENOTYPE_MAP.get(gene, {})

    if not stars:
        return "Unknown"

    phenotypes = [mapping.get(star, "Unknown") for star in stars]

    # Simplified logic:
    if "PM" in phenotypes:
        return "PM"
    if "IM" in phenotypes:
        return "IM"
    if "Decreased" in phenotypes:
        return "Decreased"
    if "Poor" in phenotypes:
        return "Poor"
    if "Normal" in phenotypes:
        return "Normal"
    if "NM" in phenotypes:
        return "NM"

    return "Unknown"
