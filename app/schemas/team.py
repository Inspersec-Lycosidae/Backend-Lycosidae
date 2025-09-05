"""
Schemas relacionados a equipes
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
import re

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
