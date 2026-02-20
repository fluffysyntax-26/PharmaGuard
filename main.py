import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import your route modules here (adjust based on your actual router names)
# from app.routes import validate, full_analysis, explanation, profile, risk

app = FastAPI(title="PharmaGuard API")

# --- 1. Configure CORS (Critical for frontend-backend communication) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Include API Routers ---
# Ensure your API routes are registered BEFORE the static files
# app.include_router(validate.router)
# app.include_router(full_analysis.router)
# app.include_router(explanation.router)
# app.include_router(profile.router)
# app.include_router(risk.router)

# --- 3. Configure Frontend Static File Serving ---
# Resolve the absolute path to the Frontend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend")

# Route the root URL ("/") to serve the landing page
@app.get("/")
async def serve_landing_page():
    landing_path = os.path.join(FRONTEND_DIR, "landing.html")
    return FileResponse(landing_path)

# Mount the entire Frontend directory to "/" to catch everything else
# This automatically serves analysis.html, app.js, and any CSS files
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")