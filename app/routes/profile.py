from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vcf_parser import parse_vcf
from app.services.phenotype_engine import build_profile

router = APIRouter()

@router.post("/extract-profile")
async def extract_profile(file: UploadFile = File(...)):
    content = await file.read()

    try:
        variants = parse_vcf(content.decode("utf-8"))
        profile = build_profile(variants)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return profile
