"""
Rotas relacionadas aos times
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import TeamCreateDTO, TeamReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException
    from ..security import SecurityUtils
except ImportError:
    from schemas import TeamCreateDTO, TeamReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException
    from security import SecurityUtils

logger = get_logger(__name__)
router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/",
            description="Create Team Endpoint",
            summary="Create Team Endpoint",
            response_model=TeamReadDTO,
            status_code=201)
@rate_limit_middleware("create_team", 10)
def create_team_endpoint(team_data: TeamCreateDTO, request: Request):
    logger.info(f"Creating team: {team_data.name}")
    
    team_data.name = SecurityUtils.sanitize_input(team_data.name)
    team_data.competition = SecurityUtils.sanitize_input(team_data.competition)
    team_data.creator = SecurityUtils.sanitize_input(team_data.creator)
    
    logger.info(f"Team created successfully: {team_data.name}")
    
    return TeamReadDTO(
        id="1",
        name=team_data.name,
        competition=team_data.competition,
        creator=team_data.creator,
        score=team_data.score or 0
    )

@router.get("/{team_id}",
           description="Get Team Endpoint",
           summary="Get Team Endpoint",
           response_model=TeamReadDTO)
@rate_limit_middleware("get_team", 60)
def get_team_endpoint(team_id: str, request: Request):
    logger.info(f"Getting team: {team_id}")
    
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    logger.info(f"Team retrieved: {team_id}")
    
    return TeamReadDTO(
        id=team_id,
        name="Sample Team",
        competition="Sample Competition",
        creator="Sample Creator",
        score=0
    )

@router.put("/{team_id}",
           description="Update Team Endpoint",
           summary="Update Team Endpoint",
           response_model=TeamReadDTO)
@rate_limit_middleware("update_team", 20)
def update_team_endpoint(team_id: str, team_data: TeamCreateDTO, request: Request):
    logger.info(f"Updating team: {team_id}")
    
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    team_data.name = SecurityUtils.sanitize_input(team_data.name)
    team_data.competition = SecurityUtils.sanitize_input(team_data.competition)
    team_data.creator = SecurityUtils.sanitize_input(team_data.creator)
    
    logger.info(f"Team updated successfully: {team_id}")
    
    return TeamReadDTO(
        id=team_id,
        name=team_data.name,
        competition=team_data.competition,
        creator=team_data.creator,
        score=team_data.score or 0
    )

@router.delete("/{team_id}",
             description="Delete Team Endpoint",
             summary="Delete Team Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_team", 10)
def delete_team_endpoint(team_id: str, request: Request):
    logger.info(f"Deleting team: {team_id}")
    
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    logger.info(f"Team deleted successfully: {team_id}")
    
    return {"message": "Team deleted successfully"}
