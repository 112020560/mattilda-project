from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.domain.models.payment import PaymentMethod

class PaymentBase(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Payment amount")
    payment_date: date = Field(..., description="Payment date")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    reference_number: Optional[str] = Field(None, max_length=100, description="Payment reference")
    notes: Optional[str] = Field(None, max_length=500, description="Payment notes")
    invoice_id: int = Field(..., gt=0, description="Invoice ID")

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    payment_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)
    is_confirmed: Optional[bool] = None

class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_confirmed: bool
    created_at: datetime
    updated_at: datetime