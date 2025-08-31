from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# Base schema
class SchoolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="School name")
    address: Optional[str] = Field(None, description="School address")
    phone: Optional[str] = Field(None, max_length=20, description="School phone number")
    email: Optional[EmailStr] = Field(None, description="School email")

# Schema para crear
class SchoolCreate(SchoolBase):
    pass

# Schema para actualizar
class SchoolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Schema para respuesta
class SchoolResponse(SchoolBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Schema con estudiantes incluidos
class SchoolWithStudents(SchoolResponse):
    students: List["StudentResponse"] = []