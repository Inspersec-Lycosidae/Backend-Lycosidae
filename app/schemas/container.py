"""
Schemas relacionados a containers
"""
from pydantic import BaseModel

class ContainerCreateDTO(BaseModel):
    deadline: str

class ContainerReadDTO(BaseModel):
    id: str
    deadline: str
