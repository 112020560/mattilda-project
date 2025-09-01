from .school import router as school_router
from .student import router as student_router
from .invoice import router as invoice_router
from .payment import router as payment_router
from .account_statement import router as account_statement_router

__all__ = [
    "school_router",
    "student_router", 
    "invoice_router",
    "payment_router",
    "account_statement_router"
]