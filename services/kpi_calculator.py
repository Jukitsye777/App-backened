# ============================================
# FILE: services/kpi_calculator.py
# ============================================

from config.database import get_db

def calculate_kpis(project_id: str):
    """
    Calculate Key Performance Indicators
    - Burn Rate: How fast money is being spent
    - CPI (Cost Performance Index): Planned vs Actual
    - SPI (Schedule Performance Index): Planned vs Actual time
    - Variance by Department
    """
    try:
        db = get_db()
        
        # Get budget data
        budgets = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        if not budgets.data:
            return {"error": "No budget data found"}
        
        # Calculate totals
        total_planned = sum(float(b['planned']) for b in budgets.data)
        total_committed = sum(float(b['committed']) for b in budgets.data)
        total_actual = sum(float(b['actual']) for b in budgets.data)
        
        # Burn rate (percentage of budget spent)
        burn_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0
        
        # Cost Performance Index (CPI)
        # CPI > 1 = under budget, CPI < 1 = over budget
        cpi = total_planned / total_actual if total_actual > 0 else 0
        
        # Variance by department
        variance_by_dept = {}
        for budget in budgets.data:
            dept = budget['dept']
            variance = float(budget['planned']) - float(budget['actual'])
            variance_by_dept[dept] = {
                "planned": float(budget['planned']),
                "actual": float(budget['actual']),
                "variance": variance,
                "percent_spent": (float(budget['actual']) / float(budget['planned']) * 100) if float(budget['planned']) > 0 else 0
            }
        
        # Get schedule performance
        schedules = db.table('schedules').select("*").eq('project_id', project_id).execute()
        
        schedule_stats = {
            "total_days": len(schedules.data) if schedules.data else 0,
            "completed": sum(1 for s in schedules.data if s['status'] == 'completed') if schedules.data else 0,
            "delayed": sum(1 for s in schedules.data if s['status'] == 'delayed') if schedules.data else 0
        }
        
        # Schedule Performance Index (SPI)
        spi = (schedule_stats['completed'] / schedule_stats['total_days']) if schedule_stats['total_days'] > 0 else 0
        
        return {
            "burn_rate": round(burn_rate, 2),
            "total_planned": total_planned,
            "total_committed": total_committed,
            "total_actual": total_actual,
            "variance": total_planned - total_actual,
            "cpi": round(cpi, 2),
            "spi": round(spi, 2),
            "variance_by_dept": variance_by_dept,
            "schedule_stats": schedule_stats
        }
        
    except Exception as e:
        return {"error": f"Error calculating KPIs: {str(e)}"}