# ============================================
# FILE: routes/invoice.py
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from config.database import get_db

router = APIRouter()

class InvoiceCreate(BaseModel):
    po_id: str
    amount: float
    due_date: date
    status: str = "pending"

@router.post("/")
async def create_invoice(invoice: InvoiceCreate):
    """Create invoice"""
    try:
        db = get_db()
        invoice_dict = invoice.dict()
        invoice_dict['due_date'] = str(invoice.due_date)
        result = db.table('invoices').insert(invoice_dict).execute()
        return {"invoice": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

