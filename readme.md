# PharmaGuard: Pharmacogenomic Risk Prediction System

Precision medicine algorithm developed for the **RIFT 2026 Hackathon** (Pharmacogenomics + Explainable AI Track).

PharmaGuard is an interpretable AI system that predicts patient-specific drug response risks and adverse events by combining pharmacogenomic data, genetic variants, and clinical features — while providing human-understandable AI-generated explanations.

## 🔗 Links

- **Live Demo**: https://pharmaguard-production.up.railway.app
- **LinkedIn Video Presentation**: https://www.linkedin.com/posts/ruthvik-np-519169297_rift2026-pharmaguard-pharmacogenomics-activity-7430437360489758720-0OyO?utm_source=share&utm_medium=member_android&rcm=ACoAAEe_oaUB2heXaWNKmNEZCe9ww_qaKLyo78E

## 🏗 Architecture Overview

PharmaGuard acts as a bridge between raw genomic data and actionable clinical insights. The architecture follows a seamless pipeline:

1. **Frontend Client**: A lightweight, responsive interface built with Vanilla JS and TailwindCSS captures the user's target medications and VCF file.
2. **VCF Parser & Phenotype Engine**: The FastAPI backend parses the raw VCF file, extracts clinically relevant variants (rsIDs, Star alleles), and computes the patient's diplotype and phenotype (e.g., Poor Metabolizer, Normal Metabolizer) based on established CPIC logic.
3. **Explainable AI Integration**: The clinical parameters are sent to the Google Gemini API (`gemini-2.5-flash`) to generate human-readable, biological mechanism explanations and clinical impact summaries.
4. **Result Delivery**: The processed risk assessment is returned to the frontend, displaying dynamic severity-coded alert cards with options to copy or export the clinical JSON report.

## 💻 Tech Stack

- **Frontend**: Vanilla JavaScript, HTML5, TailwindCSS (via CDN)
- **Backend**: Python 3.11, FastAPI, Uvicorn
- **AI & LLM**: Google Generative AI SDK (Gemini API)
- **Deployment**: Docker, Railway
- **Data Processing**: Custom VCF parser handling VCFv4.2 format

## 🛠 Installation Instructions

To run PharmaGuard locally, follow these steps:

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/yourusername/pharmaguard.git](https://github.com/yourusername/pharmaguard.git)
    cd pharmaguard

    ```

2.  **Set up a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    ```

3.  **Install Dependencies**
    Install the required Python packages (including `fastapi`, `uvicorn`, `google-genai`, and `python-multipart`).
    ```bash
    pip install -r requirements.txt

        ```

4.  **Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here

        ```

5.  **Run the Application**

    ```bash
    uvicorn app.main:app --reload

    ```

Navigate to `http://127.0.0.1:8000/` to view the application.

## Deployment Instructions

### Option A: Railway (Recommended)

1. Push your repository to GitHub.
2. Log into Railway and click **New Project** -> **Deploy from GitHub repo**.
3. Select your PharmaGuard repository.
4. Go to the **Variables** tab in your Railway dashboard and add:
   - `GEMINI_API_KEY`: `your_actual_api_key`

5. Railway will automatically detect the Python environment and install dependencies from `requirements.txt`. It will bind to the `$PORT` environment variable.
6. Once built, Railway will provide a live HTTPS URL.

### Option B: Docker

The project includes a ready-to-use `Dockerfile` based on `python:3.11-slim`.

1. **Build the image**:

   ```bash
   docker build -t pharmaguard .

   ```

2. **Run the container** (Exposes port 8000):

   ```bash
   docker run -p 8000:8000 --env-file .env pharmaguard

   ```

## 📖 API Documentation

### `GET /health`

Returns the operational status of the backend.
**Response**: `{"status": "PharmaGuard backend running", "message": "Ready for VCF analysis"}`

### `POST /validate-vcf`

Validates the structural integrity of an uploaded VCF file.

- **Payload**: `multipart/form-data` (file)
- **Response**: `{"valid": true, "variant_count": <int>}`

### `POST /full-analysis`

Runs the complete pharmacogenomic pipeline against the selected drugs.

- **Payload**: `multipart/form-data` (file, list of drugs e.g., "WARFARIN", "CODEINE")
- **Response**: Returns a comprehensive JSON array containing the `risk_assessment`, `pharmacogenomic_profile`, `clinical_recommendation`, and the `llm_generated_explanation` for each targeted drug.

## 🧪 Usage Examples & Sample VCFs

1. Open the Analysis Workspace.
2. Select target medications from the list (e.g., Warfarin, Codeine, Fluorouracil).
3. Upload a patient VCF file. For testing, you can use the sample files provided in the repository:
   - `test.vcf`: A minimal mock file containing CYP2D6 (*4) and CYP2C9 (*3) mutations.
   - `PATIENT_002.vcf`: Simulated patient with significant pathogenic variants.
   - `PATIENT_003.vcf`: Simulated patient data representing a different diplotype profile.
   - `TC_P1_PATIENT_001_Normal.vcf`: Simulated baseline normal patient.

4. Click **Run Analysis** to generate the AI-powered clinical report.
5. Use the **Export JSON** or **Copy JSON** buttons to extract the findings.

## 👥 Team Members

- **Deepak K**
- **Pranav C**
- **Ruthvik N P**
