from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vcf_parser import parse_vcf

router = APIRouter()

@router.post("/validate-vcf")
async def validate_vcf(file: UploadFile = File(...)):
    content = await file.read()
    try:
        variants = parse_vcf(content.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "valid": True,
        "variant_count": len(variants)
    }
