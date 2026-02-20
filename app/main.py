from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import routers
from app.routes import validate 
from app.routes import profile
from app.routes import risk
from app.routes import explanation
from app.routes import full_analysis

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PharmaGuard API",
    description="AI-powered Pharmacogenomic Risk Prediction System",
    version="1.0.0"
)

# ---------------------------
# CORS Configuration
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon; restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Frontend Path Resolution
# ---------------------------
project_root = os.path.dirname(os.path.dirname(__file__))
frontend_candidates = [
    os.path.join(project_root, "frontend"),
    os.path.join(project_root, "Frontend"),
]
frontend_path = next((path for path in frontend_candidates if os.path.exists(path)), None)

# ---------------------------
# Base Endpoints
# ---------------------------
@app.get("/health")
def health_check():
    return {
        "status": "PharmaGuard backend running",
        "message": "Ready for VCF analysis"
    }

@app.get("/")
async def serve_landing_page():
    if frontend_path:
        landing_file = os.path.join(frontend_path, "landing.html")
        if os.path.exists(landing_file):
            return FileResponse(landing_file)
    return {"message": "Frontend directory or landing.html not found"}

# ---------------------------
# Include Routers
# ---------------------------
app.include_router(validate.router)
app.include_router(profile.router)
app.include_router(risk.router)
app.include_router(explanation.router)
app.include_router(full_analysis.router)

# ---------------------------
# Static Files Configuration (must be last)
# ---------------------------
if frontend_path:
    # Mount the static directory to serve analysis.html, app.js, and CSS
    app.mount("/", StaticFiles(directory=frontend_path), name="static")