# ============================================
# FILE: routes/budget.py
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import get_db

router = APIRouter()

class BudgetCreate(BaseModel):
    project_id: str
    dept: str
    planned: float
    committed: float = 0
    actual: float = 0

@router.get("/projects/{project_id}")
async def get_project_budget(project_id: str):
    """Get budget for a project"""
    try:
        db = get_db()
        result = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        totals = {
            "planned": sum(float(b['planned']) for b in result.data),
            "committed": sum(float(b['committed']) for b in result.data),
            "actual": sum(float(b['actual']) for b in result.data)
        }
        
        return {
            "budgets": result.data,
            "totals": totals,
            "variance": totals['planned'] - totals['actual']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
