# ============================================
# FILE: routes/crew.py
# ============================================

from fastapi import APIRouter, HTTPException
from config.database import get_db

router = APIRouter()

@router.get("/")
async def get_all_crew():
    """Get all crew members"""
    try:
        db = get_db()
        result = db.table('crew').select("*").execute()
        return {
            "crew": result.data,
            "count": len(result.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

