import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()


def generate_explanation(gene, drug, phenotype, risk_label, recommendation, rsids):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Provide a clinical pharmacogenomic explanation based on:

Gene: {gene}
Drug: {drug}
Phenotype: {phenotype}
Risk Classification: {risk_label}
CPIC Recommendation: {recommendation}
Detected Variants: {', '.join(rsids)}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "biological_mechanism": {"type": "string"},
                        "clinical_impact": {"type": "string"},
                        "cpic_alignment_note": {"type": "string"},
                        "variant_citations": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "summary",
                        "biological_mechanism",
                        "clinical_impact",
                        "cpic_alignment_note",
                        "variant_citations"
                    ]
                }
            )
        )

        # 🔥 When using response_schema, output is already parsed
        return response.parsed

    except Exception as e:
        print("Gemini Error:", e)

        return {
            "summary": "Explanation currently unavailable.",
            "biological_mechanism": "N/A",
            "clinical_impact": "N/A",
            "cpic_alignment_note": "Generated using CPIC-aligned deterministic logic.",
            "variant_citations": rsids
        }
