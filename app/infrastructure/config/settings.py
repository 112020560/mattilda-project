from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://app_user:Abc..123@localhost:5432/mattilda_db"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://app_user:Abc..123@localhost:5432/mattilda_db"
    
    # App
    APP_NAME: str = "Mattilda API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"

settings = Settings()