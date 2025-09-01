from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.database import get_db
from app.domain.services.student_service import StudentService
from app.infrastructure.repositories.student_repository import SQLAlchemyStudentRepository
from app.infrastructure.repositories.school_repository import SQLAlchemySchoolRepository
from app.api.schemas.student import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["students"])

async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    student_repo = SQLAlchemyStudentRepository(db)
    school_repo = SQLAlchemySchoolRepository(db)
    return StudentService(student_repo, school_repo)

@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(
    student_data: StudentCreate,
    service: StudentService = Depends(get_student_service)
):
    """Crear nuevo estudiante"""
    try:
        student = await service.create_student(student_data)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    """Obtener estudiante por ID"""
    student = await service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/by-student-id/{student_id}", response_model=StudentResponse)
async def get_student_by_student_id(
    student_id: str,
    service: StudentService = Depends(get_student_service)
):
    """Obtener estudiante por Student ID"""
    student = await service.get_student_by_student_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/", response_model=List[StudentResponse])
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    service: StudentService = Depends(get_student_service)
):
    """Listar estudiantes con paginación"""
    students = await service.get_all_students(skip=skip, limit=limit, active_only=active_only)
    return students

@router.get("/school/{school_id}", response_model=List[StudentResponse])
async def get_students_by_school(
    school_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    service: StudentService = Depends(get_student_service)
):
    """Obtener estudiantes por escuela"""
    try:
        students = await service.get_students_by_school(
            school_id, skip=skip, limit=limit, active_only=active_only
        )
        return students
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    service: StudentService = Depends(get_student_service)
):
    """Actualizar estudiante"""
    try:
        student = await service.update_student(student_id, student_data)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    """Eliminar estudiante"""
    deleted = await service.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.patch("/{student_id}/deactivate", response_model=StudentResponse)
async def deactivate_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    """Desactivar estudiante"""
    student = await service.deactivate_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/search/", response_model=List[StudentResponse])
async def search_students(
    name: str = Query(..., min_length=1),
    school_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: StudentService = Depends(get_student_service)
):
    """Buscar estudiantes por nombre"""
    students = await service.search_students(
        name, school_id=school_id, skip=skip, limit=limit
    )
    return students

@router.patch("/{student_id}/transfer", response_model=StudentResponse)
async def transfer_student(
    student_id: int,
    new_school_id: int,
    service: StudentService = Depends(get_student_service)
):
    """Transferir estudiante a otra escuela"""
    try:
        student = await service.transfer_student(student_id, new_school_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))