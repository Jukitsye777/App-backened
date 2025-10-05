# ============================================
# FILE: services/ai_features.py
# ============================================

from config.database import get_db

def get_budget_features(project_id: str):
    """
    Prepare budget data for AI model
    Returns clean tabular data
    """
    try:
        db = get_db()
        result = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        # Format for AI consumption
        features = []
        for budget in result.data:
            features.append({
                "dept": budget['dept'],
                "planned": float(budget['planned']),
                "committed": float(budget['committed']),
                "actual": float(budget['actual']),
                "variance": float(budget['planned']) - float(budget['actual'])
            })
        
        return features
        
    except Exception as e:
        print(f"Error getting budget features: {e}")
        return []


def get_schedule_features(project_id: str):
    """
    Prepare schedule data for AI model
    """
    try:
        db = get_db()
        result = db.table('schedules').select("*").eq('project_id', project_id).execute()
        
        features = []
        for schedule in result.data:
            features.append({
                "day": schedule['day'],
                "status": schedule['status'],
                "scene": schedule.get('scene', ''),
                "location": schedule.get('location', '')
            })
        
        return features
        
    except Exception as e:
        print(f"Error getting schedule features: {e}")
        return []

