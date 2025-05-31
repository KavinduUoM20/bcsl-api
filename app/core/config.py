from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator, PostgresDsn
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BCSL API"
    
    # Authentication
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URI: PostgresDsn  # Changed from DATABASE_URL to DATABASE_URI to match your env
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: dict[str, any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields in the settings

settings = Settings()
