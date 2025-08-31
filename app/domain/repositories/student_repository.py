from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.student import Student

class StudentRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, student: Student) -> Student:
        pass
    
    @abstractmethod
    async def get_by_id(self, student_id: int) -> Optional[Student]:
        pass
    
    @abstractmethod
    async def get_by_student_id(self, student_id: str) -> Optional[Student]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Student]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        pass
    
    @abstractmethod
    async def get_by_school(self, school_id: int, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Student]:
        pass
    
    @abstractmethod
    async def update(self, student_id: int, student_data: dict) -> Optional[Student]:
        pass
    
    @abstractmethod
    async def delete(self, student_id: int) -> bool:
        pass
    
    @abstractmethod
    async def search_by_name(self, name: str, school_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Student]:
        pass