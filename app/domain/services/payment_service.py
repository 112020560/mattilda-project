from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.domain.models.payment import Payment, PaymentMethod
from app.domain.models.invoice import InvoiceStatus
from app.domain.repositories.payment_repository import PaymentRepositoryInterface
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface
from app.api.schemas.payment import PaymentCreate, PaymentUpdate

# home/falpizar/Documentos/fuentes/mattilda-project/app/domain/repositories/payment_repository.py

class PaymentService:
    def __init__(self, 
                 payment_repo: PaymentRepositoryInterface,
                 invoice_repo: InvoiceRepositoryInterface):
        self.payment_repo = payment_repo
        self.invoice_repo = invoice_repo

    async def create_payment(self, payment_data: PaymentCreate) -> Payment:
        # Verificar que la factura existe y se puede pagar
        invoice = await self.invoice_repo.get_by_id(payment_data.invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {payment_data.invoice_id} not found")
        
        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Invoice is already fully paid")
        
        if invoice.status == InvoiceStatus.CANCELLED:
            raise ValueError("Cannot pay cancelled invoice")
        
        # Verificar que no se exceda el monto de la factura
        current_paid = await self.payment_repo.get_total_by_invoice(payment_data.invoice_id)
        remaining_amount = invoice.amount - current_paid
        
        if payment_data.amount > remaining_amount:
            raise ValueError(f"Payment amount ({payment_data.amount}) exceeds remaining invoice amount ({remaining_amount})")
        
        # Crear pago
        payment = Payment(
            amount=payment_data.amount,
            payment_date=payment_data.payment_date,
            payment_method=payment_data.payment_method,
            reference_number=payment_data.reference_number,
            notes=payment_data.notes,
            invoice_id=payment_data.invoice_id
        )
        
        created_payment = await self.payment_repo.create(payment)
        
        # Verificar si la factura queda completamente pagada
        total_paid = await self.payment_repo.get_total_by_invoice(payment_data.invoice_id)
        if total_paid >= invoice.amount:
            await self.invoice_repo.update(payment_data.invoice_id, {
                "status": InvoiceStatus.PAID,
                "paid_date": payment_data.payment_date
            })
        
        return created_payment

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        return await self.payment_repo.get_by_id(payment_id)

    async def get_all_payments(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        return await self.payment_repo.get_all(skip=skip, limit=limit)

    async def get_payments_by_invoice(self, invoice_id: int) -> List[Payment]:
        # Verificar que la factura existe
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        return await self.payment_repo.get_by_invoice(invoice_id)

    async def get_payments_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        return await self.payment_repo.get_by_student(student_id, skip=skip, limit=limit)

    async def update_payment(self, payment_id: int, payment_data: PaymentUpdate) -> Optional[Payment]:
        # Verificar que el pago existe
        existing_payment = await self.payment_repo.get_by_id(payment_id)
        if not existing_payment:
            raise ValueError(f"Payment with id {payment_id} not found")
        
        update_dict = payment_data.model_dump(exclude_unset=True)
        
        # Si se cambia el monto, verificar límites
        if 'amount' in update_dict:
            invoice = await self.invoice_repo.get_by_id(existing_payment.invoice_id)
            other_payments_total = await self.payment_repo.get_total_by_invoice(existing_payment.invoice_id)
            other_payments_total -= existing_payment.amount  # Restar el pago actual
            
            if (other_payments_total + update_dict['amount']) > invoice.amount:
                raise ValueError("Updated payment amount would exceed invoice total")
        
        updated_payment = await self.payment_repo.update(payment_id, update_dict)
        
        # Recalcular estado de la factura
        if updated_payment:
            total_paid = await self.payment_repo.get_total_by_invoice(existing_payment.invoice_id)
            invoice = await self.invoice_repo.get_by_id(existing_payment.invoice_id)
            
            if total_paid >= invoice.amount and invoice.status != InvoiceStatus.PAID:
                await self.invoice_repo.update(existing_payment.invoice_id, {
                    "status": InvoiceStatus.PAID,
                    "paid_date": date.today()
                })
            elif total_paid < invoice.amount and invoice.status == InvoiceStatus.PAID:
                await self.invoice_repo.update(existing_payment.invoice_id, {
                    "status": InvoiceStatus.PENDING,
                    "paid_date": None
                })
        
        return updated_payment

    async def delete_payment(self, payment_id: int) -> bool:
        # Obtener el pago antes de eliminarlo
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment with id {payment_id} not found")
        
        # Eliminar pago
        deleted = await self.payment_repo.delete(payment_id)
        
        if deleted:
            # Recalcular estado de la factura
            total_paid = await self.payment_repo.get_total_by_invoice(payment.invoice_id)
            invoice = await self.invoice_repo.get_by_id(payment.invoice_id)
            
            if total_paid < invoice.amount and invoice.status == InvoiceStatus.PAID:
                await self.invoice_repo.update(payment.invoice_id, {
                    "status": InvoiceStatus.PENDING,
                    "paid_date": None
                })
        
        return deleted

    async def confirm_payment(self, payment_id: int) -> Optional[Payment]:
        """Confirmar un pago pendiente"""
        return await self.payment_repo.update(payment_id, {"is_confirmed": True})

    async def reject_payment(self, payment_id: int, reason: str = "") -> Optional[Payment]:
        """Rechazar un pago"""
        notes = f"REJECTED: {reason}" if reason else "REJECTED"
        return await self.payment_repo.update(payment_id, {
            "is_confirmed": False,
            "notes": notes
        })