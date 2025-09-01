from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.params import Depends
from app.domain.services.school_service import SchoolService
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.school_repository import SQLAlchemySchoolRepository



async def get_school_service(db: AsyncSession = Depends(get_db)) -> SchoolService:
    school_repo = SQLAlchemySchoolRepository(db)
    return SchoolService(school_repo)