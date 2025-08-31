from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.domain.models.invoice import Invoice, InvoiceStatus, InvoiceType
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.api.schemas.invoice import InvoiceCreate, InvoiceUpdate
import uuid

class InvoiceService:
    def __init__(self, 
                 invoice_repo: InvoiceRepositoryInterface,
                 student_repo: StudentRepositoryInterface):
        self.invoice_repo = invoice_repo
        self.student_repo = student_repo

    def _generate_invoice_number(self) -> str:
        """Generar número de factura único"""
        today = date.today()
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"INV-{today.strftime('%Y%m%d')}-{unique_id}"

    async def create_invoice(self, invoice_data: InvoiceCreate) -> Invoice:
        # Verificar que el estudiante existe y está activo
        student = await self.student_repo.get_by_id(invoice_data.student_id)
        if not student:
            raise ValueError(f"Student with id {invoice_data.student_id} not found")
        if not student.is_active:
            raise ValueError("Cannot create invoice for inactive student")
        
        # Generar número de factura único
        invoice_number = self._generate_invoice_number()
        while await self.invoice_repo.get_by_invoice_number(invoice_number):
            invoice_number = self._generate_invoice_number()
        
        # Crear nueva factura
        invoice = Invoice(
            invoice_number=invoice_number,
            description=invoice_data.description,
            amount=invoice_data.amount,
            due_date=invoice_data.due_date,
            invoice_type=invoice_data.invoice_type,
            student_id=invoice_data.student_id,
            issue_date=date.today()
        )
        
        return await self.invoice_repo.create(invoice)

    async def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        return await self.invoice_repo.get_by_id(invoice_id)

    async def get_invoice_by_number(self, invoice_number: str) -> Optional[Invoice]:
        return await self.invoice_repo.get_by_invoice_number(invoice_number)

    async def get_all_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return await self.invoice_repo.get_all(skip=skip, limit=limit)

    async def get_invoices_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        # Verificar que el estudiante existe
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        
        return await self.invoice_repo.get_by_student(student_id, skip=skip, limit=limit)

    async def get_invoices_by_school(self, school_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return await self.invoice_repo.get_by_school(school_id, skip=skip, limit=limit)

    async def get_invoices_by_status(self, status: InvoiceStatus, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return await self.invoice_repo.get_by_status(status, skip=skip, limit=limit)

    async def get_overdue_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return await self.invoice_repo.get_overdue_invoices(skip=skip, limit=limit)

    async def update_invoice(self, invoice_id: int, invoice_data: InvoiceUpdate) -> Optional[Invoice]:
        # Verificar que la factura existe
        existing_invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not existing_invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        # No permitir cambios si ya está pagada
        if existing_invoice.status == InvoiceStatus.PAID:
            raise ValueError("Cannot modify paid invoice")
        
        update_dict = invoice_data.model_dump(exclude_unset=True)
        
        # Actualizar estado a vencida si es necesario
        if 'status' not in update_dict and existing_invoice.due_date < date.today():
            update_dict['status'] = InvoiceStatus.OVERDUE
        
        return await self.invoice_repo.update(invoice_id, update_dict)

    async def mark_as_paid(self, invoice_id: int, paid_date: Optional[date] = None) -> Optional[Invoice]:
        """Marcar factura como pagada"""
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Invoice is already paid")
        
        if invoice.status == InvoiceStatus.CANCELLED:
            raise ValueError("Cannot pay cancelled invoice")
        
        return await self.invoice_repo.update(invoice_id, {
            "status": InvoiceStatus.PAID,
            "paid_date": paid_date or date.today()
        })

    async def cancel_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """Cancelar factura"""
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Cannot cancel paid invoice")
        
        return await self.invoice_repo.update(invoice_id, {
            "status": InvoiceStatus.CANCELLED
        })

    async def delete_invoice(self, invoice_id: int) -> bool:
        # Verificar que la factura no esté pagada
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Cannot delete paid invoice")
        
        return await self.invoice_repo.delete(invoice_id)

    async def get_student_account_statement(self, student_id: int) -> dict:
        # Verificar que el estudiante existe
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        
        # Obtener resumen de cuenta
        summary = await self.invoice_repo.get_student_account_summary(student_id)
        
        # Obtener facturas del estudiante
        invoices = await self.invoice_repo.get_by_student(student_id, skip=0, limit=50)
        
        return {
            "student_id": student_id,
            "student_name": student.full_name,
            "school_name": student.school.name if student.school else "N/A",
            "total_invoiced": summary["total_invoiced"],
            "total_paid": summary["total_paid"],
            "total_pending": summary["total_pending"],
            "overdue_amount": summary["overdue_amount"],
            "invoices": invoices
        }

    async def get_school_account_statement(self, school_id: int) -> dict:
        # Obtener resumen de cuenta del colegio
        summary = await self.invoice_repo.get_school_account_summary(school_id)
        
        # Obtener facturas recientes del colegio
        recent_invoices = await self.invoice_repo.get_by_school(school_id, skip=0, limit=20)
        
        return {
            "school_id": school_id,
            "total_students": summary["total_students"],
            "active_students": summary["active_students"],
            "total_invoiced": summary["total_invoiced"],
            "total_paid": summary["total_paid"],
            "total_pending": summary["total_pending"],
            "overdue_amount": summary["overdue_amount"],
            "recent_invoices": recent_invoices
        }