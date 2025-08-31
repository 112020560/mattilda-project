from .school_repository import SchoolRepositoryInterface
from .student_repository import StudentRepositoryInterface
from .invoice_repository import InvoiceRepositoryInterface
from .payment_repository import PaymentRepositoryInterface

__all__ = [
    "SchoolRepositoryInterface",
    "StudentRepositoryInterface", 
    "InvoiceRepositoryInterface",
    "PaymentRepositoryInterface"
]