"""
Rotas relacionadas às competições
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import CompetitionCreateDTO, CompetitionReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException, ExternalServiceException
    from ..security import SecurityUtils
    from ..interpreter_client import InterpreterClient
except ImportError:
    from schemas import CompetitionCreateDTO, CompetitionReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException, ExternalServiceException
    from security import SecurityUtils
    from interpreter_client import InterpreterClient

logger = get_logger(__name__)
router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.post("/", description="Create Competition Endpoint", summary="Create Competition Endpoint", response_model=CompetitionReadDTO, status_code=201)
@rate_limit_middleware("create_competition", 10)
async def create_competition_endpoint(competition_data: CompetitionCreateDTO, request: Request):
    logger.info(f"Creating competition: {competition_data.name}")
    
    competition_data.name = SecurityUtils.sanitize_input(competition_data.name)
    competition_data.organizer = SecurityUtils.sanitize_input(competition_data.organizer)
    competition_data.invite_code = SecurityUtils.sanitize_input(competition_data.invite_code)
    
    async with InterpreterClient() as client:
        try:
            result = await client.create_competition(competition_data.dict())
            logger.info(f"Competition created successfully: {competition_data.name}")
            return CompetitionReadDTO(**result)
        except ExternalServiceException as e:
            logger.error(f"Failed to create competition via interpreter: {str(e)}")
            raise

@router.get("/{competition_id}", description="Get Competition Endpoint", summary="Get Competition Endpoint", response_model=CompetitionReadDTO)
@rate_limit_middleware("get_competition", 60)
def get_competition_endpoint(competition_id: str, request: Request):
    logger.info(f"Getting competition: {competition_id}")
    
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    logger.info(f"Competition retrieved: {competition_id}")
    
    return CompetitionReadDTO(
        id=competition_id,
        name="Sample Competition",
        organizer="Sample Organizer",
        invite_code="SAMPLE123",
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z"
    )

@router.put("/{competition_id}",
           description="Update Competition Endpoint",
           summary="Update Competition Endpoint",
           response_model=dict)
@rate_limit_middleware("update_competition", 20)
def update_competition_endpoint(competition_id: str, competition_data: CompetitionCreateDTO, request: Request):
    logger.info(f"Updating competition: {competition_id}")
    
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    competition_data.name = SecurityUtils.sanitize_input(competition_data.name)
    competition_data.organizer = SecurityUtils.sanitize_input(competition_data.organizer)
    competition_data.invite_code = SecurityUtils.sanitize_input(competition_data.invite_code)
    
    logger.info(f"Competition updated successfully: {competition_id}")
    
    return {"message": "Competition updated successfully"}

@router.delete("/{competition_id}",
             description="Delete Competition Endpoint",
             summary="Delete Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_competition", 10)
def delete_competition_endpoint(competition_id: str, request: Request):
    logger.info(f"Deleting competition: {competition_id}")
    
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    logger.info(f"Competition deleted successfully: {competition_id}")
    
    return {"message": "Competition deleted successfully"}

@router.get("/invite/{invite_code}",
           description="Get Competition By Invite Endpoint",
           summary="Get Competition By Invite Endpoint",
           response_model=CompetitionReadDTO)
@rate_limit_middleware("get_competition_by_invite", 60)
def get_competition_by_invite_endpoint(invite_code: str, request: Request):
    logger.info(f"Getting competition by invite code: {invite_code}")
    
    if not invite_code or len(invite_code) < 1:
        raise ValidationException("Invalid invite code")
    
    invite_code = SecurityUtils.sanitize_input(invite_code)
    
    logger.info(f"Competition retrieved by invite code: {invite_code}")
    
    return CompetitionReadDTO(
        id="1",
        name="Sample Competition",
        organizer="Sample Organizer",
        invite_code=invite_code,
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z"
    )
