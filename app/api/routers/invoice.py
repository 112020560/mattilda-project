from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.infrastructure.database.database import get_db
from app.domain.services.invoice_service import InvoiceService
from app.infrastructure.repositories.invoice_repository import SQLAlchemyInvoiceRepository
from app.infrastructure.repositories.student_repository import SQLAlchemyStudentRepository
from app.domain.models.invoice import InvoiceStatus
from app.api.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["invoices"])

async def get_invoice_service(db: AsyncSession = Depends(get_db)) -> InvoiceService:
    invoice_repo = SQLAlchemyInvoiceRepository(db)
    student_repo = SQLAlchemyStudentRepository(db)
    return InvoiceService(invoice_repo, student_repo)

@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(
    invoice_data: InvoiceCreate,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Crear nueva factura"""
    try:
        invoice = await service.create_invoice(invoice_data)
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener factura por ID"""
    invoice = await service.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/by-number/{invoice_number}", response_model=InvoiceResponse)
async def get_invoice_by_number(
    invoice_number: str,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener factura por número"""
    invoice = await service.get_invoice_by_number(invoice_number)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: InvoiceService = Depends(get_invoice_service)
):
    """Listar facturas con paginación"""
    invoices = await service.get_all_invoices(skip=skip, limit=limit)
    return invoices

@router.get("/student/{student_id}", response_model=List[InvoiceResponse])
async def get_invoices_by_student(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener facturas por estudiante"""
    try:
        invoices = await service.get_invoices_by_student(
            student_id, skip=skip, limit=limit
        )
        return invoices
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/school/{school_id}", response_model=List[InvoiceResponse])
async def get_invoices_by_school(
    school_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener facturas por escuela"""
    invoices = await service.get_invoices_by_school(
        school_id, skip=skip, limit=limit
    )
    return invoices

@router.get("/status/{status}", response_model=List[InvoiceResponse])
async def get_invoices_by_status(
    status: InvoiceStatus,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener facturas por estado"""
    invoices = await service.get_invoices_by_status(
        status, skip=skip, limit=limit
    )
    return invoices

@router.get("/overdue/list", response_model=List[InvoiceResponse])
async def get_overdue_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: InvoiceService = Depends(get_invoice_service)
):
    """Obtener facturas vencidas"""
    invoices = await service.get_overdue_invoices(skip=skip, limit=limit)
    return invoices

@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Actualizar factura"""
    try:
        invoice = await service.update_invoice(invoice_id, invoice_data)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{invoice_id}/mark-paid", response_model=InvoiceResponse)
async def mark_invoice_as_paid(
    invoice_id: int,
    paid_date: date = None,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Marcar factura como pagada"""
    try:
        invoice = await service.mark_as_paid(invoice_id, paid_date)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{invoice_id}/cancel", response_model=InvoiceResponse)
async def cancel_invoice(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Cancelar factura"""
    try:
        invoice = await service.cancel_invoice(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """Eliminar factura"""
    try:
        deleted = await service.delete_invoice(invoice_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return {"message": "Invoice deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))