"""
Schemas relacionados a competições
"""
from pydantic import BaseModel, Field, validator
import re

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
