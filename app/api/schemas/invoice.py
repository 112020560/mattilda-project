from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.domain.models.invoice import InvoiceStatus, InvoiceType

class InvoiceBase(BaseModel):
    description: Optional[str] = Field(None, max_length=500, description="Invoice description")
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Invoice amount")
    due_date: date = Field(..., description="Invoice due date")
    invoice_type: InvoiceType = Field(default=InvoiceType.TUITION, description="Type of invoice")
    student_id: int = Field(..., gt=0, description="Student ID")

class InvoiceCreate(InvoiceBase):
    @validator('due_date')
    def due_date_validation(cls, v):
        if v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v

class InvoiceUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=500)
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    due_date: Optional[date] = None
    status: Optional[InvoiceStatus] = None
    invoice_type: Optional[InvoiceType] = None

class InvoiceResponse(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    invoice_number: str
    issue_date: date
    paid_date: Optional[date] = None
    status: InvoiceStatus
    created_at: datetime
    updated_at: datetime
    is_overdue: bool
    paid_amount: Decimal
    pending_amount: Decimal

class InvoiceWithStudent(InvoiceResponse):
    student: "StudentResponse"

class InvoiceWithPayments(InvoiceResponse):
    payments: List["PaymentResponse"] = []