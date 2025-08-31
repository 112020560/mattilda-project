from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal
from datetime import date

class StudentAccountStatement(BaseModel):
    student_id: int
    student_name: str
    school_name: str
    total_invoiced: Decimal
    total_paid: Decimal
    total_pending: Decimal
    overdue_amount: Decimal
    invoices: List[InvoiceResponse]

class SchoolAccountStatement(BaseModel):
    school_id: int
    school_name: str
    total_students: int
    active_students: int
    total_invoiced: Decimal
    total_paid: Decimal
    total_pending: Decimal
    overdue_amount: Decimal
    recent_invoices: List[InvoiceResponse]