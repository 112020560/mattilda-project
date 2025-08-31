from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import Optional, List
from datetime import datetime, date

class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Student first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Student last name")
    email: Optional[EmailStr] = Field(None, description="Student email")
    phone: Optional[str] = Field(None, max_length=20, description="Student phone")
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique student identifier")
    enrollment_date: date = Field(..., description="Date when student enrolled")
    birth_date: Optional[date] = Field(None, description="Student birth date")
    school_id: int = Field(..., gt=0, description="School ID")

class StudentCreate(StudentBase):
    @validator('birth_date')
    def birth_date_must_be_in_past(cls, v):
        if v and v >= date.today():
            raise ValueError('Birth date must be in the past')
        return v
    
    @validator('enrollment_date')
    def enrollment_date_validation(cls, v):
        if v > date.today():
            raise ValueError('Enrollment date cannot be in the future')
        return v

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    birth_date: Optional[date] = None
    is_active: Optional[bool] = None
    school_id: Optional[int] = Field(None, gt=0)

class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    full_name: str

class StudentWithSchool(StudentResponse):
    school: "SchoolResponse"

class StudentWithInvoices(StudentResponse):
    invoices: List["InvoiceResponse"] = []