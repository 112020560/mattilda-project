from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.database import get_db
from app.domain.services.school_service import SchoolService
from app.infrastructure.repositories.school_repository import SQLAlchemySchoolRepository
from app.api.schemas.school import SchoolCreate, SchoolUpdate, SchoolResponse

router = APIRouter(prefix="/schools", tags=["schools"])

async def get_school_service(db: AsyncSession = Depends(get_db)) -> SchoolService:
    school_repo = SQLAlchemySchoolRepository(db)
    return SchoolService(school_repo)

@router.post("/", response_model=SchoolResponse, status_code=201)
async def create_school(
    school_data: SchoolCreate,
    service: SchoolService = Depends(get_school_service)
):
    """Crear nueva escuela"""
    try:
        school = await service.create_school(school_data)
        return school
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: int,
    service: SchoolService = Depends(get_school_service)
):
    """Obtener escuela por ID"""
    school = await service.get_school_by_id(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/", response_model=List[SchoolResponse])
async def get_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    service: SchoolService = Depends(get_school_service)
):
    """Listar escuelas con paginación"""
    schools = await service.get_all_schools(skip=skip, limit=limit, active_only=active_only)
    return schools

@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    service: SchoolService = Depends(get_school_service)
):
    """Actualizar escuela"""
    try:
        school = await service.update_school(school_id, school_data)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        return school
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{school_id}")
async def delete_school(
    school_id: int,
    service: SchoolService = Depends(get_school_service)
):
    """Eliminar escuela"""
    try:
        deleted = await service.delete_school(school_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="School not found")
        return {"message": "School deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{school_id}/deactivate", response_model=SchoolResponse)
async def deactivate_school(
    school_id: int,
    service: SchoolService = Depends(get_school_service)
):
    """Desactivar escuela"""
    school = await service.deactivate_school(school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/search/", response_model=List[SchoolResponse])
async def search_schools(
    name: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: SchoolService = Depends(get_school_service)
):
    """Buscar escuelas por nombre"""
    schools = await service.search_schools(name, skip=skip, limit=limit)
    return schools

@router.get("/{school_id}/statistics")
async def get_school_statistics(
    school_id: int,
    service: SchoolService = Depends(get_school_service)
):
    """Obtener estadísticas de la escuela"""
    try:
        stats = await service.get_school_statistics(school_id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))