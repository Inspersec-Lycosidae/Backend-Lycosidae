"""
Definição de rotas da API
"""
from fastapi import APIRouter, Request
from datetime import datetime
import time

try:
    # Imports relativos quando executado como módulo
    from .schemas import *
    from .logger import get_logger
    from .config import settings
    from .rate_limiter import rate_limit_middleware, get_rate_limit_info
    from .exceptions import *
    from .security import SecurityUtils
    from .interpreter_client import InterpreterClient
except ImportError:
    # Imports absolutos quando executado diretamente
    from schemas import *
    from logger import get_logger
    from config import settings
    from rate_limiter import rate_limit_middleware, get_rate_limit_info
    from exceptions import *
    from security import SecurityUtils
    from interpreter_client import InterpreterClient

logger = get_logger(__name__)
router = APIRouter(
    prefix="/route",
    tags=["route"]
)

system_router = APIRouter(
    prefix="/system",
    tags=["System"]
)


@router.get("/", 
           description="Root Func",
           summary="Root Func",
           response_model=dict)
@rate_limit_middleware("root", 100)
def root_func():
    """Função padrão, altere conforme necessário"""
    logger.info("Root endpoint accessed")
    return {"message": "Backend-Lycosidae API is running"}

@router.post("/register",
            description="User Register",
            summary="User Register",
            response_model=UserReadDTO,
            status_code=201)
@rate_limit_middleware("register", 5)
async def user_register(user_data: UserCreateDTO, request: Request):
    """Função para criação genérica de usuário baseada em um DTO JSON"""
    logger.info(f"User registration attempt for email: {user_data.email}")
    
    # Validações de segurança
    username_validation = SecurityUtils.validate_username(user_data.username)
    if not username_validation["is_valid"]:
        raise ValidationException("Invalid username", {"username_errors": username_validation["errors"]})
    
    password_validation = SecurityUtils.validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        raise ValidationException("Invalid password", {"password_errors": password_validation["errors"]})
    
    if not SecurityUtils.validate_email_domain(user_data.email):
        raise ValidationException("Email domain not allowed")
    
    # Sanitiza dados
    user_data.username = SecurityUtils.sanitize_input(user_data.username)
    user_data.email = SecurityUtils.sanitize_input(user_data.email)
    if user_data.phone_number:
        user_data.phone_number = SecurityUtils.sanitize_input(user_data.phone_number)
    
    # Chama o interpretador para criar o usuário
    async with InterpreterClient() as client:
        try:
            result = await client.create_user(user_data.dict())
            logger.info(f"User registration successful for: {user_data.email}")
            return UserReadDTO(**result)
        except ExternalServiceException as e:
            logger.error(f"Failed to create user via interpreter: {str(e)}")
            raise


@router.post("/competitions",
            description="Create Competition Endpoint",
            summary="Create Competition Endpoint",
            response_model=CompetitionReadDTO,
            status_code=201)
@rate_limit_middleware("create_competition", 10)
async def create_competition_endpoint(competition_data: CompetitionCreateDTO, request: Request):
    """Cria uma nova competição"""
    logger.info(f"Creating competition: {competition_data.name}")
    
    # Validações de segurança
    competition_data.name = SecurityUtils.sanitize_input(competition_data.name)
    competition_data.organizer = SecurityUtils.sanitize_input(competition_data.organizer)
    competition_data.invite_code = SecurityUtils.sanitize_input(competition_data.invite_code)
    
    # Chama o interpretador para criar a competição
    async with InterpreterClient() as client:
        try:
            result = await client.create_competition(competition_data.dict())
            logger.info(f"Competition created successfully: {competition_data.name}")
            return CompetitionReadDTO(**result)
        except ExternalServiceException as e:
            logger.error(f"Failed to create competition via interpreter: {str(e)}")
            raise

@router.get("/competitions/{competition_id}",
           description="Get Competition Endpoint",
           summary="Get Competition Endpoint",
           response_model=CompetitionReadDTO)
@rate_limit_middleware("get_competition", 60)
def get_competition_endpoint(competition_id: str, request: Request):
    """Busca uma competição pelo ID"""
    logger.info(f"Getting competition: {competition_id}")
    
    # Validação de entrada
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Competition retrieved: {competition_id}")
    
    return CompetitionReadDTO(
        id=competition_id,
        name="Sample Competition",
        organizer="Sample Organizer",
        invite_code="SAMPLE123",
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z"
    )

@router.put("/competitions/{competition_id}",
           description="Update Competition Endpoint",
           summary="Update Competition Endpoint",
           response_model=dict)
@rate_limit_middleware("update_competition", 20)
def update_competition_endpoint(competition_id: str, competition_data: CompetitionCreateDTO, request: Request):
    """Atualiza uma competição existente"""
    logger.info(f"Updating competition: {competition_id}")
    
    # Validações de segurança
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    competition_data.name = SecurityUtils.sanitize_input(competition_data.name)
    competition_data.organizer = SecurityUtils.sanitize_input(competition_data.organizer)
    competition_data.invite_code = SecurityUtils.sanitize_input(competition_data.invite_code)
    
    # Aqui você implementaria a lógica de atualização no banco
    logger.info(f"Competition updated successfully: {competition_id}")
    
    return {"message": "Competition updated successfully"}

@router.delete("/competitions/{competition_id}",
             description="Delete Competition Endpoint",
             summary="Delete Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_competition", 10)
def delete_competition_endpoint(competition_id: str, request: Request):
    """Deleta uma competição"""
    logger.info(f"Deleting competition: {competition_id}")
    
    # Validação de entrada
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"Competition deleted successfully: {competition_id}")
    
    return {"message": "Competition deleted successfully"}

@router.get("/competitions/invite/{invite_code}",
           description="Get Competition By Invite Endpoint",
           summary="Get Competition By Invite Endpoint",
           response_model=CompetitionReadDTO)
@rate_limit_middleware("get_competition_by_invite", 60)
def get_competition_by_invite_endpoint(invite_code: str, request: Request):
    """Busca uma competição pelo código de convite"""
    logger.info(f"Getting competition by invite code: {invite_code}")
    
    # Validação de entrada
    if not invite_code or len(invite_code) < 1:
        raise ValidationException("Invalid invite code")
    
    invite_code = SecurityUtils.sanitize_input(invite_code)
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Competition retrieved by invite code: {invite_code}")
    
    return CompetitionReadDTO(
        id="1",
        name="Sample Competition",
        organizer="Sample Organizer",
        invite_code=invite_code,
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z"
    )


@router.post("/exercises",
            description="Create Exercise Endpoint",
            summary="Create Exercise Endpoint",
            response_model=ExerciseReadDTO,
            status_code=201)
@rate_limit_middleware("create_exercise", 10)
def create_exercise_endpoint(exercise_data: ExerciseCreateDTO, request: Request):
    """Cria um novo exercício"""
    logger.info(f"Creating exercise: {exercise_data.name}")
    
    # Validações de segurança
    exercise_data.link = SecurityUtils.sanitize_input(exercise_data.link)
    exercise_data.name = SecurityUtils.sanitize_input(exercise_data.name)
    exercise_data.difficulty = SecurityUtils.sanitize_input(exercise_data.difficulty)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Exercise created successfully: {exercise_data.name}")
    
    return ExerciseReadDTO(
        id="1",
        link=exercise_data.link,
        name=exercise_data.name,
        score=exercise_data.score,
        difficulty=exercise_data.difficulty,
        port=exercise_data.port
    )

@router.get("/exercises/{exercise_id}",
           description="Get Exercise Endpoint",
           summary="Get Exercise Endpoint",
           response_model=ExerciseReadDTO)
@rate_limit_middleware("get_exercise", 60)
def get_exercise_endpoint(exercise_id: str, request: Request):
    """Busca um exercício pelo ID"""
    logger.info(f"Getting exercise: {exercise_id}")
    
    # Validação de entrada
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Exercise retrieved: {exercise_id}")
    
    return ExerciseReadDTO(
        id=exercise_id,
        link="https://example.com/exercise",
        name="Sample Exercise",
        score=100,
        difficulty="Medium",
        port=8080
    )

@router.put("/exercises/{exercise_id}",
           description="Update Exercise Endpoint",
           summary="Update Exercise Endpoint",
           response_model=ExerciseReadDTO)
@rate_limit_middleware("update_exercise", 20)
def update_exercise_endpoint(exercise_id: str, exercise_data: ExerciseCreateDTO, request: Request):
    """Atualiza um exercício existente"""
    logger.info(f"Updating exercise: {exercise_id}")
    
    # Validações de segurança
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    exercise_data.link = SecurityUtils.sanitize_input(exercise_data.link)
    exercise_data.name = SecurityUtils.sanitize_input(exercise_data.name)
    exercise_data.difficulty = SecurityUtils.sanitize_input(exercise_data.difficulty)
    
    # Aqui você implementaria a lógica de atualização no banco
    logger.info(f"Exercise updated successfully: {exercise_id}")
    
    return ExerciseReadDTO(
        id=exercise_id,
        link=exercise_data.link,
        name=exercise_data.name,
        score=exercise_data.score,
        difficulty=exercise_data.difficulty,
        port=exercise_data.port
    )

@router.delete("/exercises/{exercise_id}",
             description="Delete Exercise Endpoint",
             summary="Delete Exercise Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise", 10)
def delete_exercise_endpoint(exercise_id: str, request: Request):
    """Deleta um exercício"""
    logger.info(f"Deleting exercise: {exercise_id}")
    
    # Validação de entrada
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    logger.info(f"Exercise deleted successfully: {exercise_id}")
    
    return {"message": "Exercise deleted successfully"}


@router.post("/tags",
            description="Create Tag Endpoint",
            summary="Create Tag Endpoint",
            response_model=TagReadDTO,
            status_code=201)
@rate_limit_middleware("create_tag", 10)
def create_tag_endpoint(tag_data: TagCreateDTO, request: Request):
    """Cria uma nova tag"""
    logger.info(f"Creating tag: {tag_data.type}")
    
    # Validações de segurança
    tag_data.type = SecurityUtils.sanitize_input(tag_data.type)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Tag created successfully: {tag_data.type}")
    
    return TagReadDTO(
        id="1",
        type=tag_data.type
    )

@router.get("/tags/{tag_id}",
           description="Get Tag Endpoint",
           summary="Get Tag Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("get_tag", 60)
def get_tag_endpoint(tag_id: str, request: Request):
    """Busca uma tag pelo ID"""
    logger.info(f"Getting tag: {tag_id}")
    
    # Validação de entrada
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Tag retrieved: {tag_id}")
    
    return TagReadDTO(
        id=tag_id,
        type="Sample Tag"
    )

@router.put("/tags/{tag_id}",
           description="Update Tag Endpoint",
           summary="Update Tag Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("update_tag", 20)
def update_tag_endpoint(tag_id: str, tag_data: TagCreateDTO, request: Request):
    """Atualiza uma tag existente"""
    logger.info(f"Updating tag: {tag_id}")
    
    # Validações de segurança
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    tag_data.type = SecurityUtils.sanitize_input(tag_data.type)
    
    # Aqui você implementaria a lógica de atualização no banco
    logger.info(f"Tag updated successfully: {tag_id}")
    
    return TagReadDTO(
        id=tag_id,
        type=tag_data.type
    )

@router.delete("/tags/{tag_id}",
             description="Delete Tag Endpoint",
             summary="Delete Tag Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_tag", 10)
def delete_tag_endpoint(tag_id: str, request: Request):
    """Deleta uma tag"""
    logger.info(f"Deleting tag: {tag_id}")
    
    # Validação de entrada
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"Tag deleted successfully: {tag_id}")
    
    return {"message": "Tag deleted successfully"}

@router.get("/tags/type/{tag_type}",
           description="Get Tag By Type Endpoint",
           summary="Get Tag By Type Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("get_tag_by_type", 60)
def get_tag_by_type_endpoint(tag_type: str, request: Request):
    """Busca uma tag pelo tipo"""
    logger.info(f"Getting tag by type: {tag_type}")
    
    # Validação de entrada
    if not tag_type or len(tag_type) < 1:
        raise ValidationException("Invalid tag type")
    
    tag_type = SecurityUtils.sanitize_input(tag_type)
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Tag retrieved by type: {tag_type}")
    
    return TagReadDTO(
        id="1",
        type=tag_type
    )


@router.post("/teams",
            description="Create Team Endpoint",
            summary="Create Team Endpoint",
            response_model=TeamReadDTO,
            status_code=201)
@rate_limit_middleware("create_team", 10)
def create_team_endpoint(team_data: TeamCreateDTO, request: Request):
    """Cria um novo time"""
    logger.info(f"Creating team: {team_data.name}")
    
    # Validações de segurança
    team_data.name = SecurityUtils.sanitize_input(team_data.name)
    team_data.competition = SecurityUtils.sanitize_input(team_data.competition)
    team_data.creator = SecurityUtils.sanitize_input(team_data.creator)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Team created successfully: {team_data.name}")
    
    return TeamReadDTO(
        id="1",
        name=team_data.name,
        competition=team_data.competition,
        creator=team_data.creator,
        score=team_data.score or 0
    )

@router.get("/teams/{team_id}",
           description="Get Team Endpoint",
           summary="Get Team Endpoint",
           response_model=TeamReadDTO)
@rate_limit_middleware("get_team", 60)
def get_team_endpoint(team_id: str, request: Request):
    """Busca um time pelo ID"""
    logger.info(f"Getting team: {team_id}")
    
    # Validação de entrada
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Team retrieved: {team_id}")
    
    return TeamReadDTO(
        id=team_id,
        name="Sample Team",
        competition="Sample Competition",
        creator="Sample Creator",
        score=0
    )

@router.put("/teams/{team_id}",
           description="Update Team Endpoint",
           summary="Update Team Endpoint",
           response_model=TeamReadDTO)
@rate_limit_middleware("update_team", 20)
def update_team_endpoint(team_id: str, team_data: TeamCreateDTO, request: Request):
    """Atualiza um time existente"""
    logger.info(f"Updating team: {team_id}")
    
    # Validações de segurança
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    team_data.name = SecurityUtils.sanitize_input(team_data.name)
    team_data.competition = SecurityUtils.sanitize_input(team_data.competition)
    team_data.creator = SecurityUtils.sanitize_input(team_data.creator)
    
    # Aqui você implementaria a lógica de atualização no banco
    logger.info(f"Team updated successfully: {team_id}")
    
    return TeamReadDTO(
        id=team_id,
        name=team_data.name,
        competition=team_data.competition,
        creator=team_data.creator,
        score=team_data.score or 0
    )

@router.delete("/teams/{team_id}",
             description="Delete Team Endpoint",
             summary="Delete Team Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_team", 10)
def delete_team_endpoint(team_id: str, request: Request):
    """Deleta um time"""
    logger.info(f"Deleting team: {team_id}")
    
    # Validação de entrada
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    logger.info(f"Team deleted successfully: {team_id}")
    
    return {"message": "Team deleted successfully"}


@router.post("/containers",
            description="Create Container Endpoint",
            summary="Create Container Endpoint",
            status_code=201)
@rate_limit_middleware("create_container", 10)
def create_container_endpoint(container_data: ContainerCreateDTO, request: Request):
    """Cria um novo container"""
    logger.info(f"Creating container with deadline: {container_data.deadline}")
    
    # Validações de segurança
    container_data.deadline = SecurityUtils.sanitize_input(container_data.deadline)
    
    logger.info(f"Container created successfully")
    
    return {"message": "Container created successfully"}

@router.get("/containers/{container_id}",
           description="Get Container Endpoint",
           summary="Get Container Endpoint",
           response_model=ContainerReadDTO)
@rate_limit_middleware("get_container", 60)
def get_container_endpoint(container_id: str, request: Request):
    """Busca um container pelo ID"""
    logger.info(f"Getting container: {container_id}")
    
    # Validação de entrada
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    # Aqui você implementaria a lógica de busca no banco
    logger.info(f"Container retrieved: {container_id}")
    
    return ContainerReadDTO(
        id=container_id,
        deadline="2024-12-31T23:59:59Z"
    )

@router.put("/containers/{container_id}",
           description="Update Container Endpoint",
           summary="Update Container Endpoint",
           response_model=ContainerReadDTO)
@rate_limit_middleware("update_container", 20)
def update_container_endpoint(container_id: str, container_data: ContainerCreateDTO, request: Request):
    """Atualiza um container existente"""
    logger.info(f"Updating container: {container_id}")
    
    # Validações de segurança
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    container_data.deadline = SecurityUtils.sanitize_input(container_data.deadline)
    
    # Aqui você implementaria a lógica de atualização no banco
    logger.info(f"Container updated successfully: {container_id}")
    
    return ContainerReadDTO(
        id=container_id,
        deadline=container_data.deadline
    )

@router.delete("/containers/{container_id}",
             description="Delete Container Endpoint",
             summary="Delete Container Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_container", 10)
def delete_container_endpoint(container_id: str, request: Request):
    """Deleta um container"""
    logger.info(f"Deleting container: {container_id}")
    
    # Validação de entrada
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    logger.info(f"Container deleted successfully: {container_id}")
    
    return {"message": "Container deleted successfully"}


@router.post("/user-competitions",
            description="Create User Competition Endpoint",
            summary="Create User Competition Endpoint",
            response_model=UserCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_user_competition", 10)
def create_user_competition_endpoint(user_competition_data: UserCompetitionCreateDTO, request: Request):
    """Cria um relacionamento usuário-competição"""
    logger.info(f"Creating user-competition relationship: {user_competition_data.user_id} -> {user_competition_data.competition_id}")
    
    # Validações de segurança
    user_competition_data.user_id = SecurityUtils.sanitize_input(user_competition_data.user_id)
    user_competition_data.competition_id = SecurityUtils.sanitize_input(user_competition_data.competition_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"User-competition relationship created successfully")
    
    return user_competition_data

@router.delete("/user-competitions/{user_id}/{competition_id}",
             description="Delete User Competition Endpoint",
             summary="Delete User Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_user_competition", 10)
def delete_user_competition_endpoint(user_id: str, competition_id: str, request: Request):
    """Deleta um relacionamento usuário-competição"""
    logger.info(f"Deleting user-competition relationship: {user_id} -> {competition_id}")
    
    # Validações de entrada
    if not user_id or len(user_id) < 1:
        raise ValidationException("Invalid user ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    user_id = SecurityUtils.sanitize_input(user_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"User-competition relationship deleted successfully")
    
    return {"message": "User-competition relationship deleted successfully"}

@router.post("/user-teams",
            description="Create User Team Endpoint",
            summary="Create User Team Endpoint",
            response_model=UserTeamCreateDTO,
            status_code=201)
@rate_limit_middleware("create_user_team", 10)
def create_user_team_endpoint(user_team_data: UserTeamCreateDTO, request: Request):
    """Cria um relacionamento usuário-time"""
    logger.info(f"Creating user-team relationship: {user_team_data.user_id} -> {user_team_data.team_id}")
    
    # Validações de segurança
    user_team_data.user_id = SecurityUtils.sanitize_input(user_team_data.user_id)
    user_team_data.team_id = SecurityUtils.sanitize_input(user_team_data.team_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"User-team relationship created successfully")
    
    return user_team_data

@router.delete("/user-teams/{user_id}/{team_id}",
             description="Delete User Team Endpoint",
             summary="Delete User Team Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_user_team", 10)
def delete_user_team_endpoint(user_id: str, team_id: str, request: Request):
    """Deleta um relacionamento usuário-time"""
    logger.info(f"Deleting user-team relationship: {user_id} -> {team_id}")
    
    # Validações de entrada
    if not user_id or len(user_id) < 1:
        raise ValidationException("Invalid user ID")
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    
    user_id = SecurityUtils.sanitize_input(user_id)
    team_id = SecurityUtils.sanitize_input(team_id)
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"User-team relationship deleted successfully")
    
    return {"message": "User-team relationship deleted successfully"}

@router.post("/team-competitions",
            description="Create Team Competition Endpoint",
            summary="Create Team Competition Endpoint",
            response_model=TeamCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_team_competition", 10)
def create_team_competition_endpoint(team_competition_data: TeamCompetitionCreateDTO, request: Request):
    """Cria um relacionamento time-competição"""
    logger.info(f"Creating team-competition relationship: {team_competition_data.team_id} -> {team_competition_data.competition_id}")
    
    # Validações de segurança
    team_competition_data.team_id = SecurityUtils.sanitize_input(team_competition_data.team_id)
    team_competition_data.competition_id = SecurityUtils.sanitize_input(team_competition_data.competition_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Team-competition relationship created successfully")
    
    return team_competition_data

@router.delete("/team-competitions/{team_id}/{competition_id}",
             description="Delete Team Competition Endpoint",
             summary="Delete Team Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_team_competition", 10)
def delete_team_competition_endpoint(team_id: str, competition_id: str, request: Request):
    """Deleta um relacionamento time-competição"""
    logger.info(f"Deleting team-competition relationship: {team_id} -> {competition_id}")
    
    # Validações de entrada
    if not team_id or len(team_id) < 1:
        raise ValidationException("Invalid team ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    team_id = SecurityUtils.sanitize_input(team_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"Team-competition relationship deleted successfully")
    
    return {"message": "Team-competition relationship deleted successfully"}

@router.post("/exercise-tags",
            description="Create Exercise Tag Endpoint",
            summary="Create Exercise Tag Endpoint",
            response_model=ExerciseTagCreateDTO,
            status_code=201)
@rate_limit_middleware("create_exercise_tag", 10)
def create_exercise_tag_endpoint(exercise_tag_data: ExerciseTagCreateDTO, request: Request):
    """Cria um relacionamento exercício-tag"""
    logger.info(f"Creating exercise-tag relationship: {exercise_tag_data.exercise_id} -> {exercise_tag_data.tag_id}")
    
    # Validações de segurança
    exercise_tag_data.exercise_id = SecurityUtils.sanitize_input(exercise_tag_data.exercise_id)
    exercise_tag_data.tag_id = SecurityUtils.sanitize_input(exercise_tag_data.tag_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Exercise-tag relationship created successfully")
    
    return exercise_tag_data

@router.delete("/exercise-tags/{exercise_id}/{tag_id}",
             description="Delete Exercise Tag Endpoint",
             summary="Delete Exercise Tag Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise_tag", 10)
def delete_exercise_tag_endpoint(exercise_id: str, tag_id: str, request: Request):
    """Deleta um relacionamento exercício-tag"""
    logger.info(f"Deleting exercise-tag relationship: {exercise_id} -> {tag_id}")
    
    # Validações de entrada
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    exercise_id = SecurityUtils.sanitize_input(exercise_id)
    tag_id = SecurityUtils.sanitize_input(tag_id)
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"Exercise-tag relationship deleted successfully")
    
    return {"message": "Exercise-tag relationship deleted successfully"}

@router.post("/exercise-competitions",
            description="Create Exercise Competition Endpoint",
            summary="Create Exercise Competition Endpoint",
            response_model=ExerciseCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_exercise_competition", 10)
def create_exercise_competition_endpoint(exercise_competition_data: ExerciseCompetitionCreateDTO, request: Request):
    """Cria um relacionamento exercício-competição"""
    logger.info(f"Creating exercise-competition relationship: {exercise_competition_data.exercise_id} -> {exercise_competition_data.competition_id}")
    
    # Validações de segurança
    exercise_competition_data.exercise_id = SecurityUtils.sanitize_input(exercise_competition_data.exercise_id)
    exercise_competition_data.competition_id = SecurityUtils.sanitize_input(exercise_competition_data.competition_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Exercise-competition relationship created successfully")
    
    return exercise_competition_data

@router.delete("/exercise-competitions/{exercise_id}/{competition_id}",
             description="Delete Exercise Competition Endpoint",
             summary="Delete Exercise Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise_competition", 10)
def delete_exercise_competition_endpoint(exercise_id: str, competition_id: str, request: Request):
    """Deleta um relacionamento exercício-competição"""
    logger.info(f"Deleting exercise-competition relationship: {exercise_id} -> {competition_id}")
    
    # Validações de entrada
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    exercise_id = SecurityUtils.sanitize_input(exercise_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    # Aqui você implementaria a lógica de exclusão no banco
    logger.info(f"Exercise-competition relationship deleted successfully")
    
    return {"message": "Exercise-competition relationship deleted successfully"}

@router.post("/container-competitions",
            description="Create Container Competition Endpoint",
            summary="Create Container Competition Endpoint",
            response_model=ContainerCompetitionCreateDTO,
            status_code=201)
@rate_limit_middleware("create_container_competition", 10)
def create_container_competition_endpoint(container_competition_data: ContainerCompetitionCreateDTO, request: Request):
    """Cria um relacionamento container-competição"""
    logger.info(f"Creating container-competition relationship: {container_competition_data.container_id} -> {container_competition_data.competition_id}")
    
    # Validações de segurança
    container_competition_data.container_id = SecurityUtils.sanitize_input(container_competition_data.container_id)
    container_competition_data.competition_id = SecurityUtils.sanitize_input(container_competition_data.competition_id)
    
    # Aqui você implementaria a lógica de criação no banco
    logger.info(f"Container-competition relationship created successfully")
    
    return container_competition_data

@router.delete("/container-competitions/{container_id}/{competition_id}",
             description="Delete Container Competition Endpoint",
             summary="Delete Container Competition Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_container_competition", 10)
def delete_container_competition_endpoint(container_id: str, competition_id: str, request: Request):
    """Deleta um relacionamento container-competição"""
    logger.info(f"Deleting container-competition relationship: {container_id} -> {competition_id}")
    
    # Validações de entrada
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    if not competition_id or len(competition_id) < 1:
        raise ValidationException("Invalid competition ID")
    
    container_id = SecurityUtils.sanitize_input(container_id)
    competition_id = SecurityUtils.sanitize_input(competition_id)
    
    logger.info(f"Container-competition relationship deleted successfully")
    
    return {"message": "Container-competition relationship deleted successfully"}


@system_router.get("/health", 
                  description="Health check endpoint",
                  response_model=HealthCheckDTO,
                  summary="Health Check",
                  description="Verifica o status de saúde da API e serviços dependentes")
@rate_limit_middleware("health_check", 60)  # 60 requests per minute
async def health_check(request: Request):
    """Endpoint de health check com informações detalhadas"""
    logger.info("Health check endpoint accessed")
    
    # Testa conexão com interpretador
    interpreter_status = "unknown"
    try:
        async with InterpreterClient() as client:
            result = await client.health_check()
            interpreter_status = "success" if result.get("status") == "healthy" else "error"
    except Exception as e:
        logger.warning(f"Interpreter health check failed: {str(e)}")
        interpreter_status = "error"
    
    health_data = HealthCheckDTO(
        status="healthy" if interpreter_status == "success" else "degraded",
        message="Backend is running properly" if interpreter_status == "success" else "Backend running with issues",
        service=settings.app_name,
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        database_status=interpreter_status
    )
    
    return health_data


@system_router.get("/rate-limit/info", 
                  description="Get rate limit information",
                  response_model=RateLimitInfoDTO,
                  summary="Rate Limit Info",
                  description="Retorna informações sobre rate limiting para o cliente")
def get_rate_limit_status(request: Request):
    """Retorna informações de rate limiting"""
    rate_info = get_rate_limit_info(request, "rate_limit_info")
    
    return RateLimitInfoDTO(
        limit=rate_info["limit"],
        remaining=rate_info["remaining"],
        reset_time=datetime.fromtimestamp(rate_info["reset_time"]),
        retry_after=max(0, rate_info["reset_time"] - int(time.time()))
    )

router.include_router(system_router)
