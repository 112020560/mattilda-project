from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.school import School

class SchoolRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, school: School) -> School:
        pass
    
    @abstractmethod
    async def get_by_id(self, school_id: int) -> Optional[School]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[School]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[School]:
        pass
    
    @abstractmethod
    async def update(self, school_id: int, school_data: dict) -> Optional[School]:
        pass
    
    @abstractmethod
    async def delete(self, school_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_students_count(self, school_id: int) -> int:
        pass
    
    @abstractmethod
    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[School]:
        pass