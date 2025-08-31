from typing import List, Optional
from datetime import date
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_, text
from sqlalchemy.orm import selectinload
from app.domain.models.invoice import Invoice, InvoiceStatus, InvoiceType
from app.domain.models.student import Student
from app.domain.models.school import School
from app.domain.models.payment import Payment
from app.domain.repositories.invoice_repository import InvoiceRepositoryInterface

class SQLAlchemyInvoiceRepository(InvoiceRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, invoice: Invoice) -> Invoice:
        self.session.add(invoice)
        await self.session.commit()
        await self.session.refresh(invoice)
        return invoice

    async def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        stmt = (
            select(Invoice)
            .options(
                selectinload(Invoice.student).selectinload(Student.school),
                selectinload(Invoice.payments)
            )
            .where(Invoice.id == invoice_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.student))
            .where(Invoice.invoice_number == invoice_number)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.student))
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.payments))
            .where(Invoice.student_id == student_id)
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_school(self, school_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            select(Invoice)
            .join(Student)
            .options(selectinload(Invoice.student))
            .where(Student.school_id == school_id)
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_status(self, status: InvoiceStatus, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.student))
            .where(Invoice.status == status)
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_overdue_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        today = date.today()
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.student).selectinload(Student.school))
            .where(
                and_(
                    Invoice.status == InvoiceStatus.PENDING,
                    Invoice.due_date < today
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.due_date)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.student))
            .where(
                and_(
                    Invoice.issue_date >= start_date,
                    Invoice.issue_date <= end_date
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Invoice.issue_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
        stmt = (
            update(Invoice)
            .where(Invoice.id == invoice_id)
            .values(**invoice_data)
            .returning(Invoice)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, invoice_id: int) -> bool:
        stmt = delete(Invoice).where(Invoice.id == invoice_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_student_account_summary(self, student_id: int) -> dict:
        # Obtener resumen de cuenta del estudiante
        stmt = text("""
            SELECT 
                COUNT(*) as total_invoices,
                COALESCE(SUM(amount), 0) as total_invoiced,
                COALESCE(SUM(CASE WHEN status = 'PAID' THEN amount ELSE 0 END), 0) as total_paid,
                COALESCE(SUM(CASE WHEN status = 'PENDING' THEN amount ELSE 0 END), 0) as total_pending,
                COALESCE(SUM(CASE WHEN status = 'PENDING' AND due_date < CURRENT_DATE THEN amount ELSE 0 END), 0) as overdue_amount
            FROM invoices 
            WHERE student_id = :student_id
        """)
        
        result = await self.session.execute(stmt, {"student_id": student_id})
        row = result.fetchone()
        
        return {
            "total_invoices": row.total_invoices,
            "total_invoiced": Decimal(str(row.total_invoiced)),
            "total_paid": Decimal(str(row.total_paid)),
            "total_pending": Decimal(str(row.total_pending)),
            "overdue_amount": Decimal(str(row.overdue_amount))
        }

    async def get_school_account_summary(self, school_id: int) -> dict:
        # Obtener resumen de cuenta del colegio
        stmt = text("""
            SELECT 
                COUNT(DISTINCT s.id) as total_students,
                COUNT(DISTINCT CASE WHEN s.is_active THEN s.id END) as active_students,
                COUNT(*) as total_invoices,
                COALESCE(SUM(i.amount), 0) as total_invoiced,
                COALESCE(SUM(CASE WHEN i.status = 'PAID' THEN i.amount ELSE 0 END), 0) as total_paid,
                COALESCE(SUM(CASE WHEN i.status = 'PENDING' THEN i.amount ELSE 0 END), 0) as total_pending,
                COALESCE(SUM(CASE WHEN i.status = 'PENDING' AND i.due_date < CURRENT_DATE THEN i.amount ELSE 0 END), 0) as overdue_amount
            FROM students s
            LEFT JOIN invoices i ON s.id = i.student_id
            WHERE s.school_id = :school_id
        """)
        
        result = await self.session.execute(stmt, {"school_id": school_id})
        row = result.fetchone()
        
        return {
            "total_students": row.total_students,
            "active_students": row.active_students,
            "total_invoices": row.total_invoices,
            "total_invoiced": Decimal(str(row.total_invoiced)),
            "total_paid": Decimal(str(row.total_paid)),
            "total_pending": Decimal(str(row.total_pending)),
            "overdue_amount": Decimal(str(row.overdue_amount))
        }