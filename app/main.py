from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes import validate 
from app.routes import profile
from app.routes import risk
from app.routes import explanation
from app.routes import full_analysis

from dotenv import load_dotenv
import os

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
# Health Check Endpoint
# ---------------------------
@app.get("/")
def health_check():
    return {
        "status": "PharmaGuard backend running",
        "message": "Ready for VCF analysis"
    }

# ---------------------------
# Include Routers
# ---------------------------
app.include_router(validate.router)
app.include_router(profile.router)
app.include_router(risk.router)
app.include_router(explanation.router)
app.include_router(full_analysis.router)


