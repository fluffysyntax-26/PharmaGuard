def parse_vcf(file_content: str):
    lines = file_content.splitlines()

    # Basic validation
    if not lines or not lines[0].startswith("##fileformat=VCFv4.2"):
        raise ValueError("Invalid VCF format")

    variants = []

    for line in lines:
        if line.startswith("#"):
            continue

        columns = line.strip().split('\t')
        
        # We need at least 10 columns to reach the patient data (index 9)
        if len(columns) < 10:
            continue

        info_field = columns[7]
        format_field = columns[8]
        patient_field = columns[9]

        # 1. Find the position of the Genotype (GT) in the FORMAT field
        format_parts = format_field.split(":")
        patient_parts = patient_field.split(":")
        
        try:
            gt_index = format_parts.index("GT")
            genotype = patient_parts[gt_index]
        except ValueError:
            continue # Skip if no GT field is found

        # 2. Filter out wild-type (0/0) and no-call (./.) genotypes
        if genotype in ["0/0", "0|0", "./.", ".|."]:
            continue

        # 3. Parse INFO field only for actual detected variants
        info_parts = info_field.split(";")
        info_dict = {}
        for part in info_parts:
            if "=" in part:
                key, value = part.split("=", 1)
                info_dict[key] = value

        if "GENE" in info_dict and "STAR" in info_dict and "RS" in info_dict:
            variants.append({
                "gene": info_dict["GENE"],
                "star": info_dict["STAR"],
                "rsid": info_dict["RS"],
                "genotype": genotype # Added this just in case you need it later!
            })

    return variants