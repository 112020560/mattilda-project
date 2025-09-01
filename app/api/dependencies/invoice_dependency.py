from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.domain.services.invoice_service import InvoiceService
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.invoice_repository import SQLAlchemyInvoiceRepository
from app.infrastructure.repositories.student_repository import SQLAlchemyStudentRepository


async def get_invoice_service(db: AsyncSession = Depends(get_db)) -> InvoiceService:
    invoice_repo = SQLAlchemyInvoiceRepository(db)
    student_repo = SQLAlchemyStudentRepository(db)
    return InvoiceService(invoice_repo, student_repo)