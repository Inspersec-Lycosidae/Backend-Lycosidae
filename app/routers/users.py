"""
Rotas relacionadas aos usuários
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import UserCreateDTO, UserReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException, ExternalServiceException
    from ..security import SecurityUtils
    from ..interpreter_client import InterpreterClient
except ImportError:
    from schemas import UserCreateDTO, UserReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException, ExternalServiceException
    from security import SecurityUtils
    from interpreter_client import InterpreterClient

logger = get_logger(__name__)
router = APIRouter(tags=["users"])

@router.get("/", description="Root Func", summary="Root Func", response_model=dict)
@rate_limit_middleware("root", 100)
def root_func():
    logger.info("Root endpoint accessed")
    return {"message": "Backend-Lycosidae API is running"}

@router.post("/register", description="User Register", summary="User Register", response_model=UserReadDTO, status_code=201)
@rate_limit_middleware("register", 5)
async def user_register(user_data: UserCreateDTO, request: Request):
    logger.info(f"User registration attempt for email: {user_data.email}")
    
    username_validation = SecurityUtils.validate_username(user_data.username)
    if not username_validation["is_valid"]:
        raise ValidationException("Invalid username", {"username_errors": username_validation["errors"]})
    
    password_validation = SecurityUtils.validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        raise ValidationException("Invalid password", {"password_errors": password_validation["errors"]})
    
    if not SecurityUtils.validate_email_domain(user_data.email):
        raise ValidationException("Email domain not allowed")
    
    user_data.username = SecurityUtils.sanitize_input(user_data.username)
    user_data.email = SecurityUtils.sanitize_input(user_data.email)
    if user_data.phone_number:
        user_data.phone_number = SecurityUtils.sanitize_input(user_data.phone_number)
    
    async with InterpreterClient() as client:
        try:
            result = await client.create_user(user_data.dict())
            logger.info(f"User registration successful for: {user_data.email}")
            return UserReadDTO(**result)
        except ExternalServiceException as e:
            logger.error(f"Failed to create user via interpreter: {str(e)}")
            raise
