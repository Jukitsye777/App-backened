from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import get_db
from services.gemini_ai import gemini_service

router = APIRouter()

@router.get("/health")
async def check_ai_health():
    """Check if Gemini AI is working"""
    try:
        response = gemini_service.client.models.generate_content(
            model=gemini_service.model,
            contents="Reply with: OK"
        )
        return {
            "status": "connected",
            "ai_provider": "Google Gemini",
            "message": "AI is operational"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/analyze/budget/{project_id}")
async def analyze_budget(project_id: str):
    """Get AI analysis of budget"""
    try:
        db = get_db()
        budget = db.table('budgets').select("*").eq('project_id', project_id).execute()
        
        if not budget.data:
            raise HTTPException(status_code=404, detail="No budget data")
        
        analysis = gemini_service.analyze_budget_risk(budget.data)
        return {"project_id": project_id, "analysis": analysis}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/schedule/{project_id}")
async def analyze_schedule(project_id: str):
    """Get AI analysis of schedule"""
    try:
        db = get_db()
        schedule = db.table('schedules').select("*").eq('project_id', project_id).execute()
        
        if not schedule.data:
            raise HTTPException(status_code=404, detail="No schedule data")
        
        analysis = gemini_service.analyze_schedule_risk(schedule.data)
        return {"project_id": project_id, "analysis": analysis}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/project/{project_id}")
async def analyze_project(project_id: str):
    """Get comprehensive AI analysis"""
    try:
        db = get_db()
        project = db.table('projects').select("*").eq('id', project_id).execute()
        budget = db.table('budgets').select("*").eq('project_id', project_id).execute()
        schedule = db.table('schedules').select("*").eq('project_id', project_id).execute()
        
        if not project.data or not budget.data or not schedule.data:
            raise HTTPException(status_code=404, detail="Insufficient data")
        
        analysis = gemini_service.analyze_project_overall(
            budget_data=budget.data,
            schedule_data=schedule.data,
            project_info=project.data[0]
        )
        
        return {
            "project_id": project_id,
            "project_title": project.data[0].get('title'),
            "analysis": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QuestionRequest(BaseModel):
    question: str
    project_id: str

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask Gemini AI any question"""
    try:
        db = get_db()
        budget = db.table('budgets').select("*").eq('project_id', request.project_id).execute()
        schedule = db.table('schedules').select("*").eq('project_id', request.project_id).execute()
        
        context = {"budget": budget.data, "schedule": schedule.data}
        answer = gemini_service.ask_question(request.question, context)
        
        return {"question": request.question, "answer": answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{project_id}")
async def generate_report(project_id: str):
    """Generate AI executive report"""
    try:
        db = get_db()
        project = db.table('projects').select("*").eq('id', project_id).execute()
        budget = db.table('budgets').select("*").eq('project_id', project_id).execute()
        schedule = db.table('schedules').select("*").eq('project_id', project_id).execute()
        pos = db.table('pos').select("*").eq('project_id', project_id).execute()
        
        if not project.data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_data = {
            "project": project.data[0],
            "budget": budget.data,
            "schedule": schedule.data,
            "purchase_orders": pos.data
        }
        
        report = gemini_service.generate_report(project_data)
        
        return {
            "project_id": project_id,
            "project_title": project.data[0].get('title'),
            "report": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))