"""
Schemas separados por entidades
"""

from .user import UserCreateDTO, UserReadDTO
from .competition import CompetitionCreateDTO, CompetitionReadDTO
from .exercise import ExerciseCreateDTO, ExerciseReadDTO
from .tag import TagCreateDTO, TagReadDTO
from .team import TeamCreateDTO, TeamReadDTO
from .container import ContainerCreateDTO, ContainerReadDTO
from .relationships import (
    UserCompetitionCreateDTO,
    UserTeamCreateDTO,
    TeamCompetitionCreateDTO,
    ExerciseTagCreateDTO,
    ExerciseCompetitionCreateDTO,
    ContainerCompetitionCreateDTO
)
from .system import (
    SuccessResponseDTO,
    ErrorResponseDTO,
    HealthCheckDTO,
    RateLimitInfoDTO
)

__all__ = [
    # User schemas
    "UserCreateDTO",
    "UserReadDTO",
    # Competition schemas
    "CompetitionCreateDTO",
    "CompetitionReadDTO",
    # Exercise schemas
    "ExerciseCreateDTO",
    "ExerciseReadDTO",
    # Tag schemas
    "TagCreateDTO",
    "TagReadDTO",
    # Team schemas
    "TeamCreateDTO",
    "TeamReadDTO",
    # Container schemas
    "ContainerCreateDTO",
    "ContainerReadDTO",
    # Relationship schemas
    "UserCompetitionCreateDTO",
    "UserTeamCreateDTO",
    "TeamCompetitionCreateDTO",
    "ExerciseTagCreateDTO",
    "ExerciseCompetitionCreateDTO",
    "ContainerCompetitionCreateDTO",
    # System schemas
    "SuccessResponseDTO",
    "ErrorResponseDTO",
    "HealthCheckDTO",
    "RateLimitInfoDTO"
]
