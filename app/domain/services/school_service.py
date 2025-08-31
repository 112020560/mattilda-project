from typing import List, Optional
from app.domain.models.school import School
from app.domain.repositories.school_repository import SchoolRepositoryInterface
from app.api.schemas.school import SchoolCreate, SchoolUpdate

class SchoolService:
    def __init__(self, school_repo: SchoolRepositoryInterface):
        self.school_repo = school_repo

    async def create_school(self, school_data: SchoolCreate) -> School:
        # Validar que el email no esté en uso
        if school_data.email:
            existing_school = await self.school_repo.get_by_email(school_data.email)
            if existing_school:
                raise ValueError(f"A school with email {school_data.email} already exists")
        
        # Crear nueva escuela
        school = School(
            name=school_data.name,
            address=school_data.address,
            phone=school_data.phone,
            email=school_data.email
        )
        
        return await self.school_repo.create(school)

    async def get_school_by_id(self, school_id: int) -> Optional[School]:
        return await self.school_repo.get_by_id(school_id)

    async def get_all_schools(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[School]:
        return await self.school_repo.get_all(skip=skip, limit=limit, active_only=active_only)

    async def update_school(self, school_id: int, school_data: SchoolUpdate) -> Optional[School]:
        # Verificar que la escuela existe
        existing_school = await self.school_repo.get_by_id(school_id)
        if not existing_school:
            raise ValueError(f"School with id {school_id} not found")
        
        # Validar email único si se está cambiando
        update_dict = school_data.model_dump(exclude_unset=True)
        if 'email' in update_dict and update_dict['email']:
            email_school = await self.school_repo.get_by_email(update_dict['email'])
            if email_school and email_school.id != school_id:
                raise ValueError(f"A school with email {update_dict['email']} already exists")
        
        return await self.school_repo.update(school_id, update_dict)

    async def delete_school(self, school_id: int) -> bool:
        # Verificar que no tenga estudiantes activos
        students_count = await self.school_repo.get_students_count(school_id)
        if students_count > 0:
            raise ValueError(f"Cannot delete school with {students_count} active students. Deactivate students first.")
        
        return await self.school_repo.delete(school_id)

    async def deactivate_school(self, school_id: int) -> Optional[School]:
        return await self.school_repo.update(school_id, {"is_active": False})

    async def search_schools(self, name: str, skip: int = 0, limit: int = 100) -> List[School]:
        return await self.school_repo.search_by_name(name, skip=skip, limit=limit)

    async def get_school_statistics(self, school_id: int) -> dict:
        school = await self.school_repo.get_by_id(school_id)
        if not school:
            raise ValueError(f"School with id {school_id} not found")
        
        students_count = await self.school_repo.get_students_count(school_id)
        
        return {
            "school_id": school_id,
            "school_name": school.name,
            "total_students": students_count,
            "is_active": school.is_active
        }