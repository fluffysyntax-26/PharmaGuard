import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"


def generate_explanation(gene, drug, phenotype, risk_label, recommendation, rsids):

    prompt = f"""
You are a clinical pharmacogenomics expert.

Gene: {gene}
Drug: {drug}
Phenotype: {phenotype}
Risk Classification: {risk_label}
CPIC Recommendation: {recommendation}
Detected Variants: {", ".join(rsids)}

Respond ONLY in valid JSON format with the following keys:
summary
biological_mechanism
clinical_impact
cpic_alignment_note
variant_citations

Do not include markdown formatting.
Return only JSON.
"""

    try:
        response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 600
            }
        },
        timeout=20
        )

        print("Status:", response.status_code)
        print("Response Text:", response.text)

        response.raise_for_status()

        result = response.json()

        if "candidates" not in result:
            return {"error": result}

        text_output = result["candidates"][0]["content"]["parts"][0]["text"]

        text_output = text_output.strip().replace("```json", "").replace("```", "")

        return json.loads(text_output)

    except Exception as e:
        print("EXCEPTION:", str(e))
    
    return {
        "summary": "Explanation unavailable due to service issue.",
        "biological_mechanism": "N/A",
        "clinical_impact": "N/A",
        "cpic_alignment_note": "Generated using CPIC-aligned deterministic logic.",
        "variant_citations": rsids,
        "exception": str(e)
    }

