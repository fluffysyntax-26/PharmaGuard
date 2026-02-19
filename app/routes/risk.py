from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.services.vcf_parser import parse_vcf
from app.services.phenotype_engine import build_profile
from app.services.cpic_rules import evaluate_drug_risk

router = APIRouter()

@router.post("/analyze-risk")
async def analyze_risk(
    file: UploadFile = File(...),
    drugs: List[str] = Form(...)
):
    content = await file.read()

    try:
        variants = parse_vcf(content.decode("utf-8"))
        profile = build_profile(variants)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    results = []

    for drug in drugs:
        risk = evaluate_drug_risk(drug, profile)
        results.append({
            "drug": drug,
            **risk
        })

    return {
        "results": results
    }
