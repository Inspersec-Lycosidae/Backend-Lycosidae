"""
Rotas relacionadas aos exercícios
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import ExerciseCreateDTO, ExerciseReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException
    from ..security import SecurityUtils
except ImportError:
    from schemas import ExerciseCreateDTO, ExerciseReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException
    from security import SecurityUtils

logger = get_logger(__name__)
router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/",
            description="Create Exercise Endpoint",
            summary="Create Exercise Endpoint",
            response_model=ExerciseReadDTO,
            status_code=201)
@rate_limit_middleware("create_exercise", 10)
def create_exercise_endpoint(exercise_data: ExerciseCreateDTO, request: Request):
    logger.info(f"Creating exercise: {exercise_data.name}")
    
    exercise_data.link = SecurityUtils.sanitize_input(exercise_data.link)
    exercise_data.name = SecurityUtils.sanitize_input(exercise_data.name)
    exercise_data.difficulty = SecurityUtils.sanitize_input(exercise_data.difficulty)
    
    logger.info(f"Exercise created successfully: {exercise_data.name}")
    
    return ExerciseReadDTO(
        id="1",
        link=exercise_data.link,
        name=exercise_data.name,
        score=exercise_data.score,
        difficulty=exercise_data.difficulty,
        port=exercise_data.port
    )

@router.get("/{exercise_id}",
           description="Get Exercise Endpoint",
           summary="Get Exercise Endpoint",
           response_model=ExerciseReadDTO)
@rate_limit_middleware("get_exercise", 60)
def get_exercise_endpoint(exercise_id: str, request: Request):
    logger.info(f"Getting exercise: {exercise_id}")
    
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    logger.info(f"Exercise retrieved: {exercise_id}")
    
    return ExerciseReadDTO(
        id=exercise_id,
        link="https://example.com/exercise",
        name="Sample Exercise",
        score=100,
        difficulty="Medium",
        port=8080
    )

@router.put("/{exercise_id}",
           description="Update Exercise Endpoint",
           summary="Update Exercise Endpoint",
           response_model=ExerciseReadDTO)
@rate_limit_middleware("update_exercise", 20)
def update_exercise_endpoint(exercise_id: str, exercise_data: ExerciseCreateDTO, request: Request):
    logger.info(f"Updating exercise: {exercise_id}")
    
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    exercise_data.link = SecurityUtils.sanitize_input(exercise_data.link)
    exercise_data.name = SecurityUtils.sanitize_input(exercise_data.name)
    exercise_data.difficulty = SecurityUtils.sanitize_input(exercise_data.difficulty)
    
    logger.info(f"Exercise updated successfully: {exercise_id}")
    
    return ExerciseReadDTO(
        id=exercise_id,
        link=exercise_data.link,
        name=exercise_data.name,
        score=exercise_data.score,
        difficulty=exercise_data.difficulty,
        port=exercise_data.port
    )

@router.delete("/{exercise_id}",
             description="Delete Exercise Endpoint",
             summary="Delete Exercise Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_exercise", 10)
def delete_exercise_endpoint(exercise_id: str, request: Request):
    logger.info(f"Deleting exercise: {exercise_id}")
    
    if not exercise_id or len(exercise_id) < 1:
        raise ValidationException("Invalid exercise ID")
    
    logger.info(f"Exercise deleted successfully: {exercise_id}")
    
    return {"message": "Exercise deleted successfully"}
