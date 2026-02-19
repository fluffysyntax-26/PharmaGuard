import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

# Load environment variables
load_dotenv()


def generate_explanation(gene, drug, phenotype, risk_label, recommendation, rsids):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a clinical pharmacogenomics expert.

Gene: {gene}
Drug: {drug}
Phenotype: {phenotype}
Risk Classification: {risk_label}
CPIC Recommendation: {recommendation}
Detected Variants: {', '.join(rsids)}

Respond ONLY in valid JSON with these exact keys:
summary
biological_mechanism
clinical_impact
cpic_alignment_note
variant_citations

Return strictly valid JSON. No markdown. No explanation outside JSON.
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=600,
            )
        )

        # Extract model output text
        text_output = response.text.strip()

        # Remove accidental markdown wrapping
        text_output = (
            text_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # Parse JSON safely
        explanation = json.loads(text_output)

        return explanation

    except Exception as e:
        print("Gemini Error:", e)

        # Safe fallback response
        return {
            "summary": "Explanation currently unavailable.",
            "biological_mechanism": "N/A",
            "clinical_impact": "N/A",
            "cpic_alignment_note": "Used CPIC-aligned rules for generation.",
            "variant_citations": rsids
        }
