"""
Schemas relacionados a relacionamentos entre entidades
"""
from pydantic import BaseModel

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
