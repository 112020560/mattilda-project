from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.invoice import get_invoice_service
from app.infrastructure.database.database import get_db
from app.domain.services.invoice_service import InvoiceService
from app.infrastructure.repositories.invoice_repository import SQLAlchemyInvoiceRepository
from app.infrastructure.repositories.student_repository import SQLAlchemyStudentRepository

router = APIRouter(prefix="/account-statements", tags=["account-statements"])

# async def get_invoice_service(db: AsyncSession = Depends(get_db)) -> InvoiceService:
#     invoice_repo = SQLAlchemyInvoiceRepository(db)
#     student_repo = SQLAlchemyStudentRepository(db)
#     return InvoiceService(invoice_repo, student_repo)

@router.get("/student/{student_id}")
async def get_student_account_statement(
    student_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """
    ENDPOINT REQUERIDO: Estado de Cuenta del Estudiante
    
    Devuelve el resumen financiero completo del estudiante:
    - Total facturado
    - Total pagado
    - Saldo pendiente
    - Facturas vencidas
    - Lista de facturas
    """
    try:
        statement = await service.get_student_account_statement(student_id)
        return statement
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/school/{school_id}")
async def get_school_account_statement(
    school_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """
    ENDPOINT REQUERIDO: Estado de Cuenta del Colegio
    
    Devuelve el resumen financiero completo del colegio:
    - Total de estudiantes
    - Total facturado
    - Total cobrado
    - Saldo pendiente
    - Facturas vencidas
    - Facturas recientes
    """
    try:
        statement = await service.get_school_account_statement(school_id)
        return statement
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))