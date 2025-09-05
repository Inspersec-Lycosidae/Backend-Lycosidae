"""
Schemas relacionados a tags
"""
from pydantic import BaseModel, Field, validator
import re

class TagCreateDTO(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)

    @validator('type')
    def sanitize_strings(cls, v):
        return re.sub(r'[<>"\']', '', v.strip())

class TagReadDTO(BaseModel):
    id: str
    type: str
