# ============================================
# FILE: routes/projects.py
# ============================================

from fastapi import APIRouter, HTTPException
from config.database import get_db
from services.event_bus import log_event

router = APIRouter()

@router.get("/{project_id}/summary")
async def get_project_summary(project_id: str):
    """
    Get comprehensive project summary
    """
    try:
        db = get_db()
        
        # Get project details
        project = db.table('projects').select("*").eq('id', project_id).execute()
        
        if not project.data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get budget summary
        budget = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        # Get schedule summary
        schedule = db.table('schedules').select("*").eq('project_id', project_id).execute()
        
        # Get PO summary
        pos = db.table('pos').select("*").eq('project_id', project_id).execute()
        
        # Calculate totals
        total_planned = sum(float(b['planned']) for b in budget.data) if budget.data else 0
        total_actual = sum(float(b['actual']) for b in budget.data) if budget.data else 0
        total_committed = sum(float(b['committed']) for b in budget.data) if budget.data else 0
        
        # Count schedules by status
        schedule_status = {}
        if schedule.data:
            for s in schedule.data:
                status = s.get('status', 'unknown')
                schedule_status[status] = schedule_status.get(status, 0) + 1
        
        # Build summary response
        summary = {
            "project": project.data[0],
            "budget_summary": {
                "total_planned": total_planned,
                "total_committed": total_committed,
                "total_actual": total_actual,
                "variance": total_planned - total_actual,
                "by_department": budget.data
            },
            "schedule_summary": {
                "total_days": len(schedule.data) if schedule.data else 0,
                "status_breakdown": schedule_status
            },
            "purchase_orders": {
                "total_count": len(pos.data) if pos.data else 0,
                "total_amount": sum(float(p['amount']) for p in pos.data) if pos.data else 0
            }
        }
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/")
async def list_projects():
    """Get all projects"""
    try:
        db = get_db()
        result = db.table('projects').select("*").order('created_at', desc=True).execute()
        return {"projects": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    