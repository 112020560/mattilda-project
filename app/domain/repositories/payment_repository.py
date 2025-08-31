from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.domain.models.payment import Payment, PaymentMethod

class PaymentRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        pass
    
    @abstractmethod
    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        pass
    
    @abstractmethod
    async def get_by_invoice(self, invoice_id: int) -> List[Payment]:
        pass
    
    @abstractmethod
    async def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        pass
    
    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Payment]:
        pass
    
    @abstractmethod
    async def get_by_method(self, method: PaymentMethod, skip: int = 0, limit: int = 100) -> List[Payment]:
        pass
    
    @abstractmethod
    async def update(self, payment_id: int, payment_data: dict) -> Optional[Payment]:
        pass
    
    @abstractmethod
    async def delete(self, payment_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_total_by_invoice(self, invoice_id: int) -> Decimal:
        pass