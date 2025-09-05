"""
Schemas relacionados a usuários
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
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
