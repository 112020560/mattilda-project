from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends

from app.domain.services.payment_service import PaymentService
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.invoice_repository import SQLAlchemyInvoiceRepository
from app.infrastructure.repositories.payment_repository import SQLAlchemyPaymentRepository


async def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    payment_repo = SQLAlchemyPaymentRepository(db)
    invoice_repo = SQLAlchemyInvoiceRepository(db)
    return PaymentService(payment_repo, invoice_repo)