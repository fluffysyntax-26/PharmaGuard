from collections import defaultdict
from app.config.constants import STAR_PHENOTYPE_MAP, SUPPORTED_GENES

def build_profile(variants):
    # 1. Initialize all supported genes with an empty baseline
    gene_data = {
        gene: {"stars": [], "rsids": [], "genotypes": []} 
        for gene in SUPPORTED_GENES
    }

    # 2. Collect variants per gene (only true mutations passed from parse_vcf)
    for variant in variants:
        gene = variant["gene"]
        if gene in gene_data:
            gene_data[gene]["stars"].append(variant["star"])
            gene_data[gene]["rsids"].append(variant["rsid"])
            # Safely get genotype, default to heterozygous 0/1 if missing
            gene_data[gene]["genotypes"].append(variant.get("genotype", "0/1"))

    profile = {}

    for gene, data in gene_data.items():
        stars = data["stars"]
        rsids = data["rsids"]
        genotypes = data["genotypes"]

        # 3. Build diplotype with baseline *1 logic
        if len(stars) == 0:
            # No mutations found -> Patient is Wild-Type
            diplotype_alleles = ["*1", "*1"]
            
        elif len(stars) == 1:
            # One mutation found -> Check if Heterozygous (0/1) or Homozygous (1/1)
            gt = genotypes[0]
            if gt in ["1/1", "1|1"]:
                diplotype_alleles = [stars[0], stars[0]]
            else:
                # Heterozygous means they have one normal *1 allele and one mutated allele
                diplotype_alleles = ["*1", stars[0]]
                
        else:
            # Multiple mutations found
            diplotype_alleles = [stars[0], stars[1]]

        diplotype = f"{diplotype_alleles[0]}/{diplotype_alleles[1]}"
        
        # Resolve phenotype using the two determined alleles
        phenotype = resolve_phenotype(gene, diplotype_alleles)

        profile[gene] = {
            "diplotype": diplotype,
            "phenotype": phenotype,
            "detected_variants": rsids
        }

    return profile


def resolve_phenotype(gene, alleles):
    mapping = STAR_PHENOTYPE_MAP.get(gene, {})

    if not alleles:
        return "Unknown"

    # Map each allele in the diplotype to its functional status
    phenotypes = [mapping.get(allele, "Unknown") for allele in alleles]

    # Simplified risk logic (Highest severity dominates)
    if "PM" in phenotypes:
        return "PM"
    if "Poor" in phenotypes:
        return "Poor"
    if "IM" in phenotypes:
        return "IM"
    if "Decreased" in phenotypes:
        return "Decreased"
    if "Normal" in phenotypes:
        return "Normal"
    if "NM" in phenotypes:
        return "NM"

    return "Unknown"