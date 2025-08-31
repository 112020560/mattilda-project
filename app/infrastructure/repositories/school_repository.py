from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload
from app.domain.models.school import School
from app.domain.models.student import Student
from app.domain.repositories.school_repository import SchoolRepositoryInterface

class SQLAlchemySchoolRepository(SchoolRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, school: School) -> School:
        self.session.add(school)
        await self.session.commit()
        await self.session.refresh(school)
        return school

    async def get_by_id(self, school_id: int) -> Optional[School]:
        stmt = select(School).where(School.id == school_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[School]:
        stmt = select(School).where(School.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[School]:
        stmt = select(School)
        if active_only:
            stmt = stmt.where(School.is_active == True)
        
        stmt = stmt.offset(skip).limit(limit).order_by(School.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, school_id: int, school_data: dict) -> Optional[School]:
        stmt = (
            update(School)
            .where(School.id == school_id)
            .values(**school_data)
            .returning(School)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, school_id: int) -> bool:
        stmt = delete(School).where(School.id == school_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_students_count(self, school_id: int) -> int:
        stmt = select(func.count(Student.id)).where(
            and_(Student.school_id == school_id, Student.is_active == True)
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[School]:
        stmt = (
            select(School)
            .where(School.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .order_by(School.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()