"""
Schemas relacionados ao sistema
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SuccessResponseDTO(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponseDTO(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

class HealthCheckDTO(BaseModel):
    status: str
    message: str
    service: str
    timestamp: datetime
    version: str
    database_status: str

class RateLimitInfoDTO(BaseModel):
    limit: int
    remaining: int
    reset_time: int
    retry_after: Optional[int] = None
