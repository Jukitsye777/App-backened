# ============================================
# FILE: routes/schedule.py
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import get_db

router = APIRouter()

class ScheduleCreate(BaseModel):
    project_id: str
    day: int
    scene: str
    location: str
    status: str = "planned"

@router.get("/projects/{project_id}")
async def get_project_schedule(project_id: str):
    """Get schedule for a project"""
    try:
        db = get_db()
        result = db.table('schedules').select("*").eq('project_id', project_id).order('day').execute()
        
        status_count = {}
        for item in result.data:
            status = item.get('status', 'unknown')
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            "schedule": result.data,
            "total_days": len(result.data),
            "status_breakdown": status_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

