def parse_vcf(file_content: str):
    lines = file_content.splitlines()

    if not lines[0].startswith("##fileformat=VCFv4.2"):
        raise ValueError("Invalid VCF format")

    variants = []

    for line in lines:
        if line.startswith("#"):
            continue

        columns = line.strip().split()
        if len(columns) < 8:
            continue

        info_field = columns[7]
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
                "rsid": info_dict["RS"]
            })

    return variants
