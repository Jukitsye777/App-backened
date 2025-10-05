# ============================================
# FILE: routes/auth.py
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(credentials: LoginRequest):
    """
    Simple login endpoint
    TODO: Implement proper JWT authentication with Supabase
    """
    # For hackathon demo - accept any login
    return {
        "message": "Login successful",
        "token": "demo-token-12345",
        "user": {
            "email": credentials.email
        }
    }
