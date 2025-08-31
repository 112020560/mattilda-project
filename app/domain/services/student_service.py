from typing import List, Optional
from datetime import date
from app.domain.models.student import Student
from app.domain.repositories.student_repository import StudentRepositoryInterface
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.api.schemas.student import StudentCreate, StudentUpdate

class StudentService:
    def __init__(self, 
                 student_repo: StudentRepositoryInterface, 
                 school_repo: SchoolRepositoryInterface):
        self.student_repo = student_repo
        self.school_repo = school_repo

    async def create_student(self, student_data: StudentCreate) -> Student:
        # Verificar que la escuela existe y está activa
        school = await self.school_repo.get_by_id(student_data.school_id)
        if not school:
            raise ValueError(f"School with id {student_data.school_id} not found")
        if not school.is_active:
            raise ValueError(f"Cannot enroll student in inactive school")
        
        # Validar que el student_id sea único
        existing_student = await self.student_repo.get_by_student_id(student_data.student_id)
        if existing_student:
            raise ValueError(f"A student with ID {student_data.student_id} already exists")
        
        # Validar email único si se proporciona
        if student_data.email:
            email_student = await self.student_repo.get_by_email(student_data.email)
            if email_student:
                raise ValueError(f"A student with email {student_data.email} already exists")
        
        # Crear nuevo estudiante
        student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email,
            phone=student_data.phone,
            student_id=student_data.student_id,
            enrollment_date=student_data.enrollment_date,
            birth_date=student_data.birth_date,
            school_id=student_data.school_id
        )
        
        return await self.student_repo.create(student)

    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        return await self.student_repo.get_by_id(student_id)

    async def get_student_by_student_id(self, student_id: str) -> Optional[Student]:
        return await self.student_repo.get_by_student_id(student_id)

    async def get_all_students(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        return await self.student_repo.get_all(skip=skip, limit=limit, active_only=active_only)

    async def get_students_by_school(self, school_id: int, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        # Verificar que la escuela existe
        school = await self.school_repo.get_by_id(school_id)
        if not school:
            raise ValueError(f"School with id {school_id} not found")
        
        return await self.student_repo.get_by_school(school_id, skip=skip, limit=limit, active_only=active_only)

    async def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        # Verificar que el estudiante existe
        existing_student = await self.student_repo.get_by_id(student_id)
        if not existing_student:
            raise ValueError(f"Student with id {student_id} not found")
        
        update_dict = student_data.model_dump(exclude_unset=True)
        
        # Validar email único si se está cambiando
        if 'email' in update_dict and update_dict['email']:
            email_student = await self.student_repo.get_by_email(update_dict['email'])
            if email_student and email_student.id != student_id:
                raise ValueError(f"A student with email {update_dict['email']} already exists")
        
        # Validar que la nueva escuela existe si se está cambiando
        if 'school_id' in update_dict:
            school = await self.school_repo.get_by_id(update_dict['school_id'])
            if not school:
                raise ValueError(f"School with id {update_dict['school_id']} not found")
            if not school.is_active:
                raise ValueError("Cannot transfer student to inactive school")
        
        return await self.student_repo.update(student_id, update_dict)

    async def delete_student(self, student_id: int) -> bool:
        # Aquí podrías agregar validaciones adicionales
        # como verificar si tiene facturas pendientes
        return await self.student_repo.delete(student_id)

    async def deactivate_student(self, student_id: int) -> Optional[Student]:
        return await self.student_repo.update(student_id, {"is_active": False})

    async def search_students(self, name: str, school_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Student]:
        return await self.student_repo.search_by_name(name, school_id=school_id, skip=skip, limit=limit)

    async def transfer_student(self, student_id: int, new_school_id: int) -> Optional[Student]:
        """Transferir estudiante a otra escuela"""
        # Verificar que el estudiante existe
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        
        # Verificar que la nueva escuela existe y está activa
        new_school = await self.school_repo.get_by_id(new_school_id)
        if not new_school:
            raise ValueError(f"School with id {new_school_id} not found")
        if not new_school.is_active:
            raise ValueError("Cannot transfer to inactive school")
        
        if student.school_id == new_school_id:
            raise ValueError("Student is already in this school")
        
        return await self.student_repo.update(student_id, {
            "school_id": new_school_id,
            "enrollment_date": date.today()  # Nueva fecha de inscripción
        })