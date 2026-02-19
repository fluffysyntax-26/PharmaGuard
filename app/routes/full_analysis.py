from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from datetime import datetime
import uuid

from app.services.vcf_parser import parse_vcf
from app.services.phenotype_engine import build_profile
from app.services.cpic_rules import evaluate_drug_risk
from app.services.llm_service import generate_explanation
from app.config.constants import PRIMARY_GENE_MAP


router = APIRouter()


@router.post("/full-analysis")
async def full_analysis(
    file: UploadFile = File(...),
    drugs: List[str] = Form(...)
):
    try:
        # Normalize drugs
        normalized_drugs = []
        for drug in drugs:
            if "," in drug:
                normalized_drugs.extend([d.strip().upper() for d in drug.split(",")])
            else:
                normalized_drugs.append(drug.strip().upper())

        # Parse VCF
        content = await file.read()
        variants = parse_vcf(content.decode("utf-8"))
        profile = build_profile(variants)

        patient_id = f"PATIENT_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        responses = []

        for drug in normalized_drugs:

            gene = PRIMARY_GENE_MAP.get(drug)
            risk_data = evaluate_drug_risk(drug, profile)

            phenotype = "Unknown"
            diplotype = None
            detected_variants = []

            if gene and gene in profile:
                gene_data = profile[gene]
                phenotype = gene_data["phenotype"]
                diplotype = gene_data["diplotype"]
                detected_variants = [
                    {"rsid": rs} for rs in gene_data["detected_variants"]
                ]

                explanation = generate_explanation(
                    gene=gene,
                    drug=drug,
                    phenotype=phenotype,
                    risk_label=risk_data["risk_label"],
                    recommendation=risk_data["clinical_recommendation"]["recommendation_summary"],
                    rsids=gene_data["detected_variants"]
                )
            else:
                explanation = {
                    "summary": "No pharmacogenomic data available for this drug.",
                    "biological_mechanism": "Required gene variant not detected in uploaded VCF.",
                    "clinical_impact": "Standard dosing should be considered unless other clinical factors apply.",
                    "cpic_alignment_note": "No CPIC-guided adjustment possible due to missing genotype data.",
                    "variant_citations": []
                }

            response_object = {
                "patient_id": patient_id,
                "drug": drug,
                "timestamp": timestamp,
                "risk_assessment": {
                    "risk_label": risk_data["risk_label"],
                    "confidence_score": risk_data["confidence_score"],
                    "severity": risk_data["severity"]
                },
                "pharmacogenomic_profile": {
                    "primary_gene": gene,
                    "diplotype": diplotype,
                    "phenotype": phenotype,
                    "detected_variants": detected_variants
                },
                "clinical_recommendation": risk_data["clinical_recommendation"],
                "llm_generated_explanation": explanation,
                "quality_metrics": {
                    "vcf_parsing_success": True,
                    "genes_detected": len(profile),
                    "variants_detected": len(variants)
                }
            }

            responses.append(response_object)

        return responses if len(responses) > 1 else responses[0]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))