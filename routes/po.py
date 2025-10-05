# ============================================
# FILE: routes/po.py
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import get_db

router = APIRouter()

class POCreate(BaseModel):
    project_id: str
    vendor: str
    amount: float
    status: str = "draft"

@router.post("/")
async def create_po(po: POCreate):
    """Create purchase order"""
    try:
        db = get_db()
        result = db.table('pos').insert(po.dict()).execute()
        return {"po": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/projects/{project_id}")
async def get_project_pos(project_id: str):
    """Get all POs for a project"""
    try:
        db = get_db()
        result = db.table('pos').select("*").eq('project_id', project_id).execute()
        return {
            "pos": result.data,
            "total_amount": sum(float(po['amount']) for po in result.data),
            "count": len(result.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

