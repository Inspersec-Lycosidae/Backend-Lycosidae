"""
Schemas relacionados a exercícios
"""
from pydantic import BaseModel, Field, validator
import re

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
