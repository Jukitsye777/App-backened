# ============================================
# FILE: services/event_bus.py
# ============================================

from config.database import get_db
from datetime import datetime

def log_event(project_id: str, event_type: str, payload: dict):
    """
    Log an event to the events table
    This creates an audit trail and triggers for AI processing
    """
    try:
        db = get_db()
        
        event_data = {
            "project_id": project_id,
            "type": event_type,
            "payload_json": payload,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = db.table('events').insert(event_data).execute()
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Error logging event: {e}")
        return None
