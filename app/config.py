"""
Configurações da aplicação usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
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
    
    interpreter_url: str = Field("http://localhost:8080", env="INTERPRETER_URL")
    
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_expiration: int = Field(3600, env="JWT_EXPIRATION")  # 1 hora
    
    secret_key: str = Field(..., env="SECRET_KEY")
    allowed_hosts: str = Field("localhost,127.0.0.1", env="ALLOWED_HOSTS")
    cors_origins: str = Field("http://localhost:3000", env="CORS_ORIGINS")
    
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")  # segundos
    
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    smtp_host: Optional[str] = Field(None, env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(None, env="SMTP_PASSWORD")
    smtp_tls: bool = Field(True, env="SMTP_TLS")
    
    max_file_size: int = Field(10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_file_types: str = Field(
        "image/jpeg,image/png,image/gif,application/pdf", 
        env="ALLOWED_FILE_TYPES"
    )
    
    redis_url: Optional[str] = Field(None, env="REDIS_URL")
    cache_ttl: int = Field(300, env="CACHE_TTL")  # 5 minutos
    
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special_chars: bool = True
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Retorna allowed_hosts como lista"""
        return [host.strip() for host in self.allowed_hosts.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Retorna cors_origins como lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Retorna allowed_file_types como lista"""
        return [file_type.strip() for file_type in self.allowed_file_types.split(",")]
    
    @field_validator("jwt_expiration")
    @classmethod
    def validate_jwt_expiration(cls, v):
        if v < 60:
            raise ValueError("JWT expiration must be at least 60 seconds")
        if v > 86400:
            raise ValueError("JWT expiration must not exceed 86400 seconds (24 hours)")
        return v
    
    @field_validator("rate_limit_requests")
    @classmethod
    def validate_rate_limit_requests(cls, v):
        if v < 1:
            raise ValueError("Rate limit requests must be at least 1")
        return v
    
    @field_validator("rate_limit_window")
    @classmethod
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