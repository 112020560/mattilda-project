from typing import List, Optional
from datetime import date
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.orm import selectinload
from app.domain.models.payment import Payment, PaymentMethod
from app.domain.repositories.payment_repository import PaymentRepositoryInterface

class SQLAlchemyPaymentRepository(PaymentRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payment: Payment) -> Payment:
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        stmt = (
            select(Payment)
            .options(selectinload(Payment.invoice))
            .where(Payment.id == payment_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        stmt = (
            select(Payment)
            .options(selectinload(Payment.invoice))
            .offset(skip)
            .limit(limit)
            .order_by(Payment.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_invoice(self, invoice_id: int) -> List[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.invoice_id == invoice_id)
            .order_by(Payment.payment_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_student(self, student_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        stmt = (
            select(Payment)
            .join(Payment.invoice)
            .options(selectinload(Payment.invoice))
            .where(Payment.invoice.has(student_id=student_id))
            .offset(skip)
            .limit(limit)
            .order_by(Payment.payment_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Payment]:
        stmt = (
            select(Payment)
            .options(selectinload(Payment.invoice))
            .where(
                and_(
                    Payment.payment_date >= start_date,
                    Payment.payment_date <= end_date
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Payment.payment_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_method(self, method: PaymentMethod, skip: int = 0, limit: int = 100) -> List[Payment]:
        stmt = (
            select(Payment)
            .options(selectinload(Payment.invoice))
            .where(Payment.payment_method == method)
            .offset(skip)
            .limit(limit)
            .order_by(Payment.payment_date.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, payment_id: int, payment_data: dict) -> Optional[Payment]:
        stmt = (
            update(Payment)
            .where(Payment.id == payment_id)
            .values(**payment_data)
            .returning(Payment)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, payment_id: int) -> bool:
        stmt = delete(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_total_by_invoice(self, invoice_id: int) -> Decimal:
        stmt = select(func.sum(Payment.amount)).where(
            and_(
                Payment.invoice_id == invoice_id,
                Payment.is_confirmed == True
            )
        )
        result = await self.session.execute(stmt)
        total = result.scalar()
        return Decimal(str(total)) if total else Decimal('0.00')