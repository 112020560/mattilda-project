from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.payment_dependency import get_payment_service
from app.infrastructure.database.database import get_db
from app.domain.services.payment_service import PaymentService
from app.infrastructure.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.infrastructure.repositories.invoice_repository import SQLAlchemyInvoiceRepository
from app.api.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

# async def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
#     payment_repo = SQLAlchemyPaymentRepository(db)
#     invoice_repo = SQLAlchemyInvoiceRepository(db)
#     return PaymentService(payment_repo, invoice_repo)

@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment_data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service)
):
    """Crear nuevo pago"""
    try:
        payment = await service.create_payment(payment_data)
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Obtener pago por ID"""
    payment = await service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/", response_model=List[PaymentResponse])
async def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PaymentService = Depends(get_payment_service)
):
    """Listar pagos con paginación"""
    payments = await service.get_all_payments(skip=skip, limit=limit)
    return payments

@router.get("/invoice/{invoice_id}", response_model=List[PaymentResponse])
async def get_payments_by_invoice(
    invoice_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Obtener pagos por factura"""
    try:
        payments = await service.get_payments_by_invoice(invoice_id)
        return payments
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/student/{student_id}", response_model=List[PaymentResponse])
async def get_payments_by_student(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PaymentService = Depends(get_payment_service)
):
    """Obtener pagos por estudiante"""
    payments = await service.get_payments_by_student(
        student_id, skip=skip, limit=limit
    )
    return payments

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    service: PaymentService = Depends(get_payment_service)
):
    """Actualizar pago"""
    try:
        payment = await service.update_payment(payment_id, payment_data)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{payment_id}")
async def delete_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Eliminar pago"""
    try:
        deleted = await service.delete_payment(payment_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service)
):
    """Confirmar pago"""
    payment = await service.confirm_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.patch("/{payment_id}/reject", response_model=PaymentResponse)
async def reject_payment(
    payment_id: int,
    reason: str = "",
    service: PaymentService = Depends(get_payment_service)
):
    """Rechazar pago"""
    payment = await service.reject_payment(payment_id, reason)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment