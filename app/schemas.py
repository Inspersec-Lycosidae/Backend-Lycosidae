"""
Schemas para comunicação com o interpretador
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
import re

try:
    from .logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

# User DTOs
class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    phone_number: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must contain only letters, numbers, underscores, and hyphens')
        if v.lower() in ['admin', 'root', 'administrator', 'system']:
            raise ValueError('Username not allowed')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('email')
    def validate_email_domain(cls, v):
        allowed_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'insper.edu.br']
        domain = v.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValueError('Email domain not allowed')
        return v.lower()

class UserReadDTO(BaseModel):
    id: str
    username: str
    email: str
    phone_number: Optional[str] = None

# Competition DTOs
class CompetitionCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    organizer: str = Field(..., min_length=1, max_length=100)
    invite_code: str = Field(..., min_length=6, max_length=20)
    start_date: str
    end_date: str

    @validator('name', 'organizer')
    def sanitize_strings(cls, v):
        return re.sub(r'[<>"\']', '', v.strip())

class CompetitionReadDTO(BaseModel):
    id: str
    name: str
    organizer: str
    invite_code: str
    start_date: str
    end_date: str

# Exercise DTOs
class ExerciseCreateDTO(BaseModel):
    link: str = Field(..., min_length=1, max_length=500)
    name: str = Field(..., min_length=1, max_length=100)
    score: int = Field(..., ge=0, le=1000)
    difficulty: str = Field(..., min_length=1, max_length=50)
    port: int = Field(..., ge=1, le=65535)

    @validator('name', 'difficulty')
    def sanitize_strings(cls, v):
        return re.sub(r'[<>"\']', '', v.strip())

class ExerciseReadDTO(BaseModel):
    id: str
    link: str
    name: str
    score: int
    difficulty: str
    port: int

# Tag DTOs
class TagCreateDTO(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)

    @validator('type')
    def sanitize_strings(cls, v):
        return re.sub(r'[<>"\']', '', v.strip())

class TagReadDTO(BaseModel):
    id: str
    type: str

# Team DTOs
class TeamCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    competition: str = Field(..., min_length=1, max_length=100)
    creator: str = Field(..., min_length=1, max_length=100)
    score: Optional[int] = Field(default=0, ge=0, le=10000)

    @validator('name', 'competition', 'creator')
    def sanitize_strings(cls, v):
        return re.sub(r'[<>"\']', '', v.strip())

class TeamReadDTO(BaseModel):
    id: str
    name: str
    competition: str
    creator: str
    score: int

# Container DTOs
class ContainerCreateDTO(BaseModel):
    deadline: str

class ContainerReadDTO(BaseModel):
    id: str
    deadline: str

# Relationship DTOs
class UserCompetitionCreateDTO(BaseModel):
    user_id: str
    competition_id: str

class UserTeamCreateDTO(BaseModel):
    user_id: str
    team_id: str

class TeamCompetitionCreateDTO(BaseModel):
    team_id: str
    competition_id: str

class ExerciseTagCreateDTO(BaseModel):
    exercise_id: str
    tag_id: str

class ExerciseCompetitionCreateDTO(BaseModel):
    exercise_id: str
    competition_id: str

class ContainerCompetitionCreateDTO(BaseModel):
    container_id: str
    competition_id: str

# System DTOs
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