"""
Main FastAPI Application
Film Production Management System with Gemini AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Import all route modules (including ai)
from routes import auth, projects, budget, po, invoice, schedule, crew, reports, ai

# Create FastAPI app
app = FastAPI(
    title="Film Production Management API",
    description="Backend API for film production tracking and management with Gemini AI",
    version="1.0.0"
)

# CORS middleware - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "Film Production Management API with Gemini AI",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include all route modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(budget.router, prefix="/budget", tags=["Budget"])
app.include_router(po.router, prefix="/pos", tags=["Purchase Orders"])
app.include_router(invoice.router, prefix="/invoices", tags=["Invoices"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])
app.include_router(crew.router, prefix="/crew", tags=["Crew"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(ai.router, prefix="/ai", tags=["AI Analysis"])  # AI endpoints

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (for development)
    )