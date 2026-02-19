from fastapi import APIRouter
from app.services.llm_service import generate_explanation

router = APIRouter()

@router.post("/generate-explanation")
def generate(payload: dict):

    result = generate_explanation(
        gene=payload["gene"],
        drug=payload["drug"],
        phenotype=payload["phenotype"],
        risk_label=payload["risk_label"],
        recommendation=payload["recommendation"],
        rsids=payload["rsids"]
    )

    return result
