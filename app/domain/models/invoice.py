from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from enum import Enum
from decimal import Decimal

class InvoiceStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"

class InvoiceType(str, Enum):
    TUITION = "TUITION"
    REGISTRATION = "REGISTRATION"
    MATERIALS = "MATERIALS"
    TRANSPORT = "TRANSPORT"
    FOOD = "FOOD"
    EXTRA = "EXTRA"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Fechas
    issue_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    paid_date = Column(Date, nullable=True)
    
    # Status y tipo
    status = Column(SQLEnum(InvoiceStatus), nullable=False, default=InvoiceStatus.PENDING, index=True)
    invoice_type = Column(SQLEnum(InvoiceType), nullable=False, default=InvoiceType.TUITION)
    
    # Foreign Keys
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")
    
    @property
    def is_overdue(self):
        from datetime import date
        return self.status == InvoiceStatus.PENDING and self.due_date < date.today()
    
    @property
    def paid_amount(self):
        return sum(payment.amount for payment in self.payments if payment.is_confirmed)
    
    @property
    def pending_amount(self):
        return self.amount - self.paid_amount
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.invoice_number}', amount={self.amount}, status='{self.status}')>"