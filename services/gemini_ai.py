"""
Gemini AI Service
Connects your backend to Google Gemini AI for predictions and insights
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Gemini
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: google-genai not installed. Install with: pip install google-genai")
    GEMINI_AVAILABLE = False

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    if not GEMINI_API_KEY:
        print("⚠️  Warning: GEMINI_API_KEY not found in .env file")

class GeminiAIService:
    """Service to use Gemini AI for film production predictions"""
    
    def __init__(self):
        self.client = client
        self.model = "gemini-2.0-flash-exp"
    
    def analyze_budget_risk(self, budget_data):
        """
        Analyze budget risk using Gemini AI
        """
        if not self.client:
            return {
                "error": "Gemini AI not configured",
                "risk_level": "unknown",
                "risk_percentage": 0,
                "predicted_overrun": 0,
                "at_risk_departments": [],
                "recommendations": ["Configure GEMINI_API_KEY in .env"],
                "summary": "AI service unavailable"
            }
        
        try:
            prompt = f"""
You are a film production financial analyst. Analyze this budget data and provide risk assessment.

Budget Data:
{json.dumps(budget_data, indent=2)}

Analyze and provide:
1. Overall risk level (low/medium/high)
2. Risk percentage (0-100)
3. Predicted budget overrun amount
4. Top 3 specific recommendations
5. Which departments are at highest risk

Respond ONLY with valid JSON in this exact format (no markdown, no extra text):
{{
    "risk_level": "low",
    "risk_percentage": 0,
    "predicted_overrun": 0,
    "at_risk_departments": [],
    "recommendations": [],
    "summary": ""
}}
"""
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse response
            response_text = response.text.strip()
            
            # Clean markdown if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result
            
        except Exception as e:
            print(f"Error with Gemini AI: {e}")
            return {
                "error": str(e),
                "risk_level": "unknown",
                "risk_percentage": 0,
                "predicted_overrun": 0,
                "at_risk_departments": [],
                "recommendations": ["Unable to get AI analysis"],
                "summary": "AI service error"
            }
    
    def analyze_schedule_risk(self, schedule_data):
        """
        Analyze schedule delays using Gemini AI
        """
        if not self.client:
            return {
                "error": "Gemini AI not configured",
                "delay_risk": "unknown",
                "estimated_delay_days": 0,
                "completion_percentage": 0,
                "problem_areas": [],
                "recommendations": ["Configure GEMINI_API_KEY"],
                "summary": "AI service unavailable"
            }
        
        try:
            prompt = f"""
You are a film production scheduling expert. Analyze this shooting schedule and predict delays.

Schedule Data:
{json.dumps(schedule_data, indent=2)}

Analyze and provide:
1. Delay risk level (low/medium/high)
2. Estimated delay in days
3. Completion percentage
4. Problem scenes/days
5. Top 3 recommendations

Respond ONLY with valid JSON (no markdown):
{{
    "delay_risk": "low",
    "estimated_delay_days": 0,
    "completion_percentage": 0,
    "problem_areas": [],
    "recommendations": [],
    "summary": ""
}}
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            response_text = response.text.strip()
            
            # Clean markdown
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result
            
        except Exception as e:
            print(f"Error with Gemini AI: {e}")
            return {
                "error": str(e),
                "delay_risk": "unknown",
                "estimated_delay_days": 0,
                "completion_percentage": 0,
                "problem_areas": [],
                "recommendations": ["Unable to get AI analysis"],
                "summary": "AI service error"
            }
    
    def analyze_project_overall(self, budget_data, schedule_data, project_info=None):
        """
        Comprehensive project analysis using Gemini AI
        """
        if not self.client:
            return {
                "error": "Gemini AI not configured",
                "project_health": "unknown",
                "overall_risk_score": 0,
                "budget_forecast": {"status": "unknown", "predicted_final_cost": 0, "variance": 0},
                "schedule_forecast": {"status": "unknown", "delay_days": 0},
                "top_recommendations": ["Configure GEMINI_API_KEY in .env"],
                "key_risks": [],
                "executive_summary": "AI service unavailable"
            }
        
        try:
            # Calculate basic stats
            total_planned = sum(float(b.get('planned', 0)) for b in budget_data)
            total_actual = sum(float(b.get('actual', 0)) for b in budget_data)
            total_days = len(schedule_data)
            completed_days = sum(1 for s in schedule_data if s.get('status') == 'completed')
            
            prompt = f"""
You are an expert film production consultant. Analyze this project comprehensively.

PROJECT STATS:
- Budget Planned: ${total_planned:,.2f}
- Budget Spent: ${total_actual:,.2f}
- Total Days: {total_days}
- Days Completed: {completed_days}

BUDGET BREAKDOWN:
{json.dumps(budget_data, indent=2)}

SCHEDULE STATUS:
{json.dumps(schedule_data, indent=2)}

Provide comprehensive analysis. Respond ONLY with valid JSON (no markdown):
{{
    "project_health": "good",
    "overall_risk_score": 0,
    "budget_forecast": {{
        "status": "on budget",
        "predicted_final_cost": 0,
        "variance": 0
    }},
    "schedule_forecast": {{
        "status": "on schedule",
        "predicted_completion_date": "",
        "delay_days": 0
    }},
    "top_recommendations": [],
    "key_risks": [],
    "executive_summary": ""
}}
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            response_text = response.text.strip()
            
            # Clean markdown
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result
            
        except Exception as e:
            print(f"Error with Gemini AI: {e}")
            return {
                "error": str(e),
                "project_health": "unknown",
                "overall_risk_score": 0,
                "executive_summary": "Unable to perform AI analysis",
                "top_recommendations": ["AI service error"]
            }
    
    def ask_question(self, question, context_data):
        """
        Ask Gemini AI any question about your project
        """
        if not self.client:
            return "Gemini AI not configured. Please add GEMINI_API_KEY to .env file."
        
        try:
            prompt = f"""
You are a film production expert. Answer this question based on the project data.

Question: {question}

Project Data:
{json.dumps(context_data, indent=2)}

Provide a clear, concise, actionable answer (2-3 sentences).
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_report(self, project_data):
        """
        Generate executive report using Gemini AI
        """
        if not self.client:
            return "Gemini AI not configured. Please add GEMINI_API_KEY to .env file."
        
        try:
            prompt = f"""
You are a film production executive. Write a professional project status report.

Project Data:
{json.dumps(project_data, indent=2)}

Write a concise executive summary (3-4 paragraphs) covering:
1. Current project status
2. Budget performance
3. Schedule performance
4. Key risks and recommendations

Use professional business language.
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating report: {str(e)}"


# Create singleton instance
gemini_service = GeminiAIService()


# Test function
def test_gemini():
    """Test Gemini connection"""
    if not client:
        print("❌ Gemini client not initialized. Check GEMINI_API_KEY in .env")
        return False
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Say 'Hello, Gemini is connected!' in one sentence"
        )
        print("✅ Gemini AI Connected!")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing Gemini AI connection...")
    test_gemini()