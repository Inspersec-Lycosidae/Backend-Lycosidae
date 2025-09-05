"""
Configurações da aplicação usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    app_name: str = "Backend-Lycosidae"
    app_version: str = "1.0.0"
    debug: bool = False
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    interpreter_url: str = Field("http://localhost:8001", env="INTERPRETER_URL")
    
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_expiration: int = Field(3600, env="JWT_EXPIRATION")  # 1 hora
    
    secret_key: str = Field(..., env="SECRET_KEY")
    allowed_hosts: List[str] = Field(["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(["http://localhost:3000"], env="CORS_ORIGINS")
    
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")  # segundos
    
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    smtp_host: Optional[str] = Field(None, env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(None, env="SMTP_PASSWORD")
    smtp_tls: bool = Field(True, env="SMTP_TLS")
    
    max_file_size: int = Field(10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_file_types: List[str] = Field(
        ["image/jpeg", "image/png", "image/gif", "application/pdf"], 
        env="ALLOWED_FILE_TYPES"
    )
    
    redis_url: Optional[str] = Field(None, env="REDIS_URL")
    cache_ttl: int = Field(300, env="CACHE_TTL")  # 5 minutos
    
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special_chars: bool = True
    
    @validator("allowed_hosts", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_file_types", pre=True)
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    @validator("jwt_expiration")
    def validate_jwt_expiration(cls, v):
        if v < 60:
            raise ValueError("JWT expiration must be at least 60 seconds")
        if v > 86400:
            raise ValueError("JWT expiration must not exceed 86400 seconds (24 hours)")
        return v
    
    @validator("rate_limit_requests")
    def validate_rate_limit_requests(cls, v):
        if v < 1:
            raise ValueError("Rate limit requests must be at least 1")
        return v
    
    @validator("rate_limit_window")
    def validate_rate_limit_window(cls, v):
        if v < 1:
            raise ValueError("Rate limit window must be at least 1 second")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()

def validate_settings():
    """Valida se as configurações críticas estão definidas"""
    critical_settings = [
        ("JWT_SECRET", settings.jwt_secret),
        ("SECRET_KEY", settings.secret_key),
    ]
    
    missing_settings = []
    for setting_name, setting_value in critical_settings:
        if not setting_value or setting_value in ["your-super-secret-jwt-key-here-change-this-in-production", "your-super-secret-key-here-change-this-in-production"]:
            missing_settings.append(setting_name)
    
    if missing_settings:
        raise ValueError(f"Missing or invalid critical settings: {', '.join(missing_settings)}")
    
    return True