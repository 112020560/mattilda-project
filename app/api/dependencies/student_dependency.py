from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.domain.services.student_service import StudentService
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.school_repository import SQLAlchemySchoolRepository
from app.infrastructure.repositories.student_repository import SQLAlchemyStudentRepository


async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    student_repo = SQLAlchemyStudentRepository(db)
    school_repo = SQLAlchemySchoolRepository(db)
    return StudentService(student_repo, school_repo)