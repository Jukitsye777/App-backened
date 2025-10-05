# App-backened


hey there jaice here


                                                

Film Production Management System - Backend API

## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Supabase credentials
5. Run: `python main.py`

## API Endpoints

- `POST /auth/login` - Authentication
- `GET /projects/{id}/summary` - Project overview
- `GET /projects/{id}/budget` - Budget details
- `POST /pos` - Create purchase order
- `POST /invoices` - Create invoice
- `GET /projects/{id}/schedule` - Schedule
- `GET /crew` - Crew list
- `GET /reports/kpis` - KPI metrics

## Development

Run server: `uvicorn main:app --reload`