from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.domain.models.invoice import Invoice, InvoiceStatus, InvoiceType

class InvoiceRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, invoice: Invoice) -> Invoice:
        pass
    
    @abstractmethod
    async def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        pass
    
    @abstractmethod
    async def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def get_by_school(self, school_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def get_by_status(self, status: InvoiceStatus, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def get_overdue_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Invoice]:
        pass
    
    @abstractmethod
    async def update(self, invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
        pass
    
    @abstractmethod
    async def delete(self, invoice_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_student_account_summary(self, student_id: int) -> dict:
        pass
    
    @abstractmethod
    async def get_school_account_summary(self, school_id: int) -> dict:
        pass