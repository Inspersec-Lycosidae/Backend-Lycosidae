"""
Rotas relacionadas aos usuários
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import UserCreateDTO, UserReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException, ExternalServiceException
    from ..security import SecurityUtils, InputValidator, PasswordManager
    from ..interpreter_client import InterpreterClient
except ImportError:
    from schemas import UserCreateDTO, UserReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException, ExternalServiceException
    from security import SecurityUtils, InputValidator, PasswordManager
    from interpreter_client import InterpreterClient

logger = get_logger(__name__)
router = APIRouter(tags=["users"])

@router.get("/", description="Root Func", summary="Root Func", response_model=dict)
@rate_limit_middleware("root", 100)
def root_func():
    logger.info("Root endpoint accessed")
    return {"message": "Backend-Lycosidae API is running"}

@router.post("/debug-register", description="Debug Register", summary="Debug Register")
@rate_limit_middleware("debug_register", 100)
async def debug_register(request: Request):
    """Endpoint para debug - mostra exatamente o que está sendo recebido"""
    try:
        body = await request.body()
        headers = dict(request.headers)
        content_type = request.headers.get("content-type", "")
        
        logger.info(f"Debug register - Content-Type: {content_type}")
        logger.info(f"Debug register - Body: {body}")
        logger.info(f"Debug register - Headers: {headers}")
        
        return {
            "content_type": content_type,
            "body_raw": body.decode('utf-8') if body else "",
            "body_length": len(body) if body else 0,
            "headers": headers
        }
    except Exception as e:
        logger.error(f"Debug register error: {str(e)}")
        return {"error": str(e)}

@router.post("/register-temp", description="Temp User Register", summary="Temp User Register", status_code=201)
@rate_limit_middleware("register_temp", 5)
async def user_register_temp(user_data: dict, request: Request):
    """Endpoint temporário para debug - aceita dict diretamente"""
    logger.info(f"Temp register received data: {user_data}")
    logger.info(f"Temp register data type: {type(user_data)}")
    
    try:
        # Tentar criar UserCreateDTO manualmente
        user_dto = UserCreateDTO(**user_data)
        logger.info(f"Successfully created UserCreateDTO: {user_dto}")
        return {"message": "Data received successfully", "data": user_data}
    except Exception as e:
        logger.error(f"Error creating UserCreateDTO: {str(e)}")
        return {"error": str(e), "received_data": user_data}

@router.post("/register", description="User Register", summary="User Register", response_model=UserReadDTO, status_code=201)
@rate_limit_middleware("register", 5)
async def user_register(user_data: UserCreateDTO, request: Request):
    logger.info(f"User registration attempt for email: {user_data.email}")
    
    username_validation = InputValidator.validate_username(user_data.username)
    if not username_validation["is_valid"]:
        raise ValidationException("Invalid username", {"username_errors": username_validation["errors"]})
    
    password_validation = PasswordManager.validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        raise ValidationException("Invalid password", {"password_errors": password_validation["errors"]})
    
    if not InputValidator.validate_email_domain(user_data.email):
        raise ValidationException("Email domain not allowed")
    
    user_data.username = InputValidator.sanitize_input(user_data.username)
    user_data.email = InputValidator.sanitize_input(user_data.email)
    if user_data.phone_number:
        user_data.phone_number = InputValidator.sanitize_input(user_data.phone_number)
    
    async with InterpreterClient() as client:
        try:
            result = await client.create_user(user_data.dict())
            logger.info(f"User registration successful for: {user_data.email}")
            return UserReadDTO(**result)
        except ExternalServiceException as e:
            logger.error(f"Failed to create user via interpreter: {str(e)}")
            raise
