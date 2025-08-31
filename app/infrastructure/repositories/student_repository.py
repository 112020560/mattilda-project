from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.orm import selectinload
from app.domain.models.student import Student
from app.domain.models.school import School
from app.domain.repositories.student_repository import StudentRepositoryInterface

class SQLAlchemyStudentRepository(StudentRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def get_by_id(self, student_id: int) -> Optional[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.school))
            .where(Student.id == student_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_id(self, student_id: str) -> Optional[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.school))
            .where(Student.student_id == student_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Student]:
        stmt = select(Student).where(Student.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        stmt = select(Student).options(selectinload(Student.school))
        if active_only:
            stmt = stmt.where(Student.is_active == True)
        
        stmt = stmt.offset(skip).limit(limit).order_by(Student.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_school(self, school_id: int, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        stmt = select(Student).where(Student.school_id == school_id)
        if active_only:
            stmt = stmt.where(Student.is_active == True)
        
        stmt = stmt.offset(skip).limit(limit).order_by(Student.first_name, Student.last_name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, student_id: int, student_data: dict) -> Optional[Student]:
        stmt = (
            update(Student)
            .where(Student.id == student_id)
            .values(**student_data)
            .returning(Student)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, student_id: int) -> bool:
        stmt = delete(Student).where(Student.id == student_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def search_by_name(self, name: str, school_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Student]:
        full_name_concat = func.concat(Student.first_name, ' ', Student.last_name)
        stmt = select(Student).where(
            or_(
                Student.first_name.ilike(f"%{name}%"),
                Student.last_name.ilike(f"%{name}%"),
                full_name_concat.ilike(f"%{name}%")
            )
        )
        
        if school_id:
            stmt = stmt.where(Student.school_id == school_id)
        
        stmt = stmt.offset(skip).limit(limit).order_by(Student.first_name, Student.last_name)
        result = await self.session.execute(stmt)
        return result.scalars().all()