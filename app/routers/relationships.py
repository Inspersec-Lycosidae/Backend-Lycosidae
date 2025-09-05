"""
Rotas relacionadas aos relacionamentos entre entidades
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import (
        UserCompetitionCreateDTO, UserTeamCreateDTO, TeamCompetitionCreateDTO,
        ExerciseTagCreateDTO, ExerciseCompetitionCreateDTO, ContainerCompetitionCreateDTO
    )
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException
    from ..security import SecurityUtils
except ImportError:
    from schemas import (
        UserCompetitionCreateDTO, UserTeamCreateDTO, TeamCompetitionCreateDTO,
        ExerciseTagCreateDTO, ExerciseCompetitionCreateDTO, ContainerCompetitionCreateDTO
    )
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException
    from security import SecurityUtils

logger = get_logger(__name__)
router = APIRouter(tags=["relationships"])

# User-Competition Relationships
@router.post("/user-competitions",
            description="Create User Competition Endpoint",
            summary="Create User Competition Endpoint",
            response_model=UserCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_user_competition", 10)
def create_user_competition_endpoint(user_competition_data: UserCompetitionCreateDTO, request: Request):
    logger.info(f"Creating user-competition relationship: {user_competition_data.user_id} -> {user_competition_data.competition_id}")
    
    user_competition_data.user_id = SecurityUtils.sanitize_input(user_competition_data.user_id)
    user_competition_data.competition_id = SecurityUtils.sanitize_input(user_competition_data.competition_id)
    
    logger.info(f"User-competition relationship created successfully")
    
    return user_competition_data

@router.delete("/user-competitions/{user_id}/{competition_id}",
             description="Delete User Competition Endpoint",
             summary="Delete User Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_user_competition", 10)
def delete_user_competition_endpoint(user_id: str, competition_id: str, request: Request):
    logger.info(f"Deleting user-competition relationship: {user_id} -> {competition_id}")
    
    if not user_id or len(user_id) < 1:
        raise ValidationException("Invalid user ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    user_id = SecurityUtils.sanitize_input(user_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    logger.info(f"User-competition relationship deleted successfully")
    
    return {"message": "User-competition relationship deleted successfully"}

# User-Team Relationships
@router.post("/user-teams",
            description="Create User Team Endpoint",
            summary="Create User Team Endpoint",
            response_model=UserTeamCreateDTO,
            status_code=201)
@rate_limit_middleware("create_user_team", 10)
def create_user_team_endpoint(user_team_data: UserTeamCreateDTO, request: Request):
    logger.info(f"Creating user-team relationship: {user_team_data.user_id} -> {user_team_data.team_id}")
    
    user_team_data.user_id = SecurityUtils.sanitize_input(user_team_data.user_id)
    user_team_data.team_id = SecurityUtils.sanitize_input(user_team_data.team_id)
    
    logger.info(f"User-team relationship created successfully")
    
    return user_team_data

@router.delete("/user-teams/{user_id}/{team_id}",
             description="Delete User Team Endpoint",
             summary="Delete User Team Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_user_team", 10)
def delete_user_team_endpoint(user_id: str, team_id: str, request: Request):
    logger.info(f"Deleting user-team relationship: {user_id} -> {team_id}")
    
    if not user_id or len(user_id) < 1:
        raise ValidationException("Invalid user ID")
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    user_id = SecurityUtils.sanitize_input(user_id)
    team_id = SecurityUtils.sanitize_input(team_id)
    
    logger.info(f"User-team relationship deleted successfully")
    
    return {"message": "User-team relationship deleted successfully"}

# Team-Competition Relationships
@router.post("/team-competitions",
            description="Create Team Competition Endpoint",
            summary="Create Team Competition Endpoint",
            response_model=TeamCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_team_competition", 10)
def create_team_competition_endpoint(team_competition_data: TeamCompetitionCreateDTO, request: Request):
    logger.info(f"Creating team-competition relationship: {team_competition_data.team_id} -> {team_competition_data.competition_id}")
    
    team_competition_data.team_id = SecurityUtils.sanitize_input(team_competition_data.team_id)
    team_competition_data.competition_id = SecurityUtils.sanitize_input(team_competition_data.competition_id)
    
    logger.info(f"Team-competition relationship created successfully")
    
    return team_competition_data

@router.delete("/team-competitions/{team_id}/{competition_id}",
             description="Delete Team Competition Endpoint",
             summary="Delete Team Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_team_competition", 10)
def delete_team_competition_endpoint(team_id: str, competition_id: str, request: Request):
    logger.info(f"Deleting team-competition relationship: {team_id} -> {competition_id}")
    
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    team_id = SecurityUtils.sanitize_input(team_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    logger.info(f"Team-competition relationship deleted successfully")
    
    return {"message": "Team-competition relationship deleted successfully"}

# Exercise-Tag Relationships
@router.post("/exercise-tags",
            description="Create Exercise Tag Endpoint",
            summary="Create Exercise Tag Endpoint",
            response_model=ExerciseTagCreateDTO,
            status_code=201)
@rate_limit_middleware("create_exercise_tag", 10)
def create_exercise_tag_endpoint(exercise_tag_data: ExerciseTagCreateDTO, request: Request):
    logger.info(f"Creating exercise-tag relationship: {exercise_tag_data.exercise_id} -> {exercise_tag_data.tag_id}")
    
    exercise_tag_data.exercise_id = SecurityUtils.sanitize_input(exercise_tag_data.exercise_id)
    exercise_tag_data.tag_id = SecurityUtils.sanitize_input(exercise_tag_data.tag_id)
    
    logger.info(f"Exercise-tag relationship created successfully")
    
    return exercise_tag_data

@router.delete("/exercise-tags/{exercise_id}/{tag_id}",
             description="Delete Exercise Tag Endpoint",
             summary="Delete Exercise Tag Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise_tag", 10)
def delete_exercise_tag_endpoint(exercise_id: str, tag_id: str, request: Request):
    logger.info(f"Deleting exercise-tag relationship: {exercise_id} -> {tag_id}")
    
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    exercise_id = SecurityUtils.sanitize_input(exercise_id)
    tag_id = SecurityUtils.sanitize_input(tag_id)
    
    logger.info(f"Exercise-tag relationship deleted successfully")
    
    return {"message": "Exercise-tag relationship deleted successfully"}

# Exercise-Competition Relationships
@router.post("/exercise-competitions",
            description="Create Exercise Competition Endpoint",
            summary="Create Exercise Competition Endpoint",
            response_model=ExerciseCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_exercise_competition", 10)
def create_exercise_competition_endpoint(exercise_competition_data: ExerciseCompetitionCreateDTO, request: Request):
    logger.info(f"Creating exercise-competition relationship: {exercise_competition_data.exercise_id} -> {exercise_competition_data.competition_id}")
    
    exercise_competition_data.exercise_id = SecurityUtils.sanitize_input(exercise_competition_data.exercise_id)
    exercise_competition_data.competition_id = SecurityUtils.sanitize_input(exercise_competition_data.competition_id)
    
    logger.info(f"Exercise-competition relationship created successfully")
    
    return exercise_competition_data

@router.delete("/exercise-competitions/{exercise_id}/{competition_id}",
             description="Delete Exercise Competition Endpoint",
             summary="Delete Exercise Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise_competition", 10)
def delete_exercise_competition_endpoint(exercise_id: str, competition_id: str, request: Request):
    logger.info(f"Deleting exercise-competition relationship: {exercise_id} -> {competition_id}")
    
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    exercise_id = SecurityUtils.sanitize_input(exercise_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    logger.info(f"Exercise-competition relationship deleted successfully")
    
    return {"message": "Exercise-competition relationship deleted successfully"}

# Container-Competition Relationships
@router.post("/container-competitions",
            description="Create Container Competition Endpoint",
            summary="Create Container Competition Endpoint",
            response_model=ContainerCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_container_competition", 10)
def create_container_competition_endpoint(container_competition_data: ContainerCompetitionCreateDTO, request: Request):
    logger.info(f"Creating container-competition relationship: {container_competition_data.container_id} -> {container_competition_data.competition_id}")
    
    container_competition_data.container_id = SecurityUtils.sanitize_input(container_competition_data.container_id)
    container_competition_data.competition_id = SecurityUtils.sanitize_input(container_competition_data.competition_id)
    
    logger.info(f"Container-competition relationship created successfully")
    
    return container_competition_data

@router.delete("/container-competitions/{container_id}/{competition_id}",
             description="Delete Container Competition Endpoint",
             summary="Delete Container Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_container_competition", 10)
def delete_container_competition_endpoint(container_id: str, competition_id: str, request: Request):
    logger.info(f"Deleting container-competition relationship: {container_id} -> {competition_id}")
    
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    container_id = SecurityUtils.sanitize_input(container_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    logger.info(f"Container-competition relationship deleted successfully")
    
    return {"message": "Container-competition relationship deleted successfully"}
