from .invoice_dependency import get_invoice_service
from .payment_dependency import get_payment_service
from .student_dependency import get_student_service
from .school_dependency import get_school_service

__all__ = [
    "get_invoice_service",
    "get_payment_service",
    "get_student_service",
    "get_school_service"
]