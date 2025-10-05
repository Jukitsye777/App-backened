# ============================================
# FILE: routes/reports.py
# ============================================

from fastapi import APIRouter, HTTPException
from config.database import get_db

router = APIRouter()

@router.get("/kpis")
async def get_kpis(project_id: str = None):
    """Get KPI metrics"""
    try:
        db = get_db()
        
        if not project_id:
            return {"message": "Please provide project_id parameter"}
        
        # Get budget data
        budgets = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        if not budgets.data:
            return {"message": "No budget data found"}
        
        # Calculate metrics
        total_planned = sum(float(b['planned']) for b in budgets.data)
        total_actual = sum(float(b['actual']) for b in budgets.data)
        
        burn_rate = total_actual / total_planned if total_planned > 0 else 0
        variance = total_planned - total_actual
        
        # Variance by department
        variance_by_dept = {}
        for b in budgets.data:
            dept = b['dept']
            variance_by_dept[dept] = float(b['planned']) - float(b['actual'])
        
        return {
            "burn_rate": round(burn_rate, 2),
            "total_planned": total_planned,
            "total_actual": total_actual,
            "variance": variance,
            "variance_by_dept": variance_by_dept,
            "CPI": round(total_planned / total_actual, 2) if total_actual > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")