"""
Sistema de tratamento de exceções personalizadas
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Dict, Any, Optional
import traceback
import logging

try:
    from .logger import get_logger
    from .schemas import ErrorResponseDTO
except ImportError:
    from logger import get_logger
    from schemas import ErrorResponseDTO

logger = get_logger(__name__)

class BaseAPIException(Exception):
    """Exceção base para a API"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

class ValidationException(BaseAPIException):
    """Exceção para erros de validação"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details
        )

class AuthenticationException(BaseAPIException):
    """Exceção para erros de autenticação"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR"
        )

class AuthorizationException(BaseAPIException):
    """Exceção para erros de autorização"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR"
        )

class NotFoundException(BaseAPIException):
    """Exceção para recursos não encontrados"""
    
    def __init__(self, message: str = "Resource not found", resource: str = "Resource"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details={"resource": resource}
        )

class ConflictException(BaseAPIException):
    """Exceção para conflitos de recursos"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT"
        )

class RateLimitException(BaseAPIException):
    """Exceção para rate limit excedido"""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        details = {}
        if retry_after is not None:
            details["retry_after"] = retry_after
        
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )

class DatabaseException(BaseAPIException):
    """Exceção para erros de banco de dados"""
    
    def __init__(self, message: str = "Database error"):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR"
        )

class ExternalServiceException(BaseAPIException):
    """Exceção para erros de serviços externos"""
    
    def __init__(self, message: str = "External service error", service: Optional[str] = None):
        details = {}
        if service:
            details["service"] = service
        
        super().__init__(
            message=message,
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )

class BusinessLogicException(BaseAPIException):
    """Exceção para erros de lógica de negócio"""
    
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code="BUSINESS_LOGIC_ERROR"
        )

def create_error_response(
    message: str,
    status_code: int = 500,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """Cria resposta de erro padronizada"""
    error_response = ErrorResponseDTO(
        success=False,
        message=message,
        error_code=error_code or "UNKNOWN_ERROR",
        details=details or {}
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler para erros de validação do Pydantic"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    # Formata erros de validação de forma mais amigável
    formatted_errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        formatted_errors.append(f"{field}: {message}")
    
    return create_error_response(
        message="Validation error",
        status_code=422,
        error_code="VALIDATION_ERROR",
        details={"validation_errors": formatted_errors}
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handler para exceções HTTP do FastAPI"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    return create_error_response(
        message=str(exc.detail),
        status_code=exc.status_code,
        error_code="HTTP_ERROR"
    )

async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handler para exceções HTTP do Starlette"""
    logger.warning(f"Starlette HTTP exception: {exc.status_code} - {exc.detail}")
    
    return create_error_response(
        message=str(exc.detail),
        status_code=exc.status_code,
        error_code="HTTP_ERROR"
    )

async def base_api_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """Handler para exceções personalizadas da API"""
    logger.error(f"API exception: {exc.error_code} - {exc.message}")
    
    return create_error_response(
        message=exc.message,
        status_code=exc.status_code,
        error_code=exc.error_code,
        details=exc.details
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler para exceções gerais não tratadas"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Em produção, não expor detalhes internos
    message = "Internal server error"
    details = {}
    
    # Em desenvolvimento, incluir mais detalhes
    import os
    if os.getenv("DEBUG", "false").lower() == "true":
        message = str(exc)
        details = {
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exc()
        }
    
    return create_error_response(
        message=message,
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
        details=details
    )

def setup_exception_handlers(app):
    """Configura handlers de exceção na aplicação"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
    app.add_exception_handler(BaseAPIException, base_api_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("Exception handlers configured")

class ErrorLogger:
    """Logger especializado para erros"""
    
    @staticmethod
    def log_error(
        error: Exception,
        request: Request,
        user_id: Optional[int] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """Log estruturado de erros"""
        context = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "request_url": str(request.url),
            "request_method": request.method,
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
        }
        
        if user_id:
            context["user_id"] = user_id
        
        if additional_context:
            context.update(additional_context)
        
        logger.error(f"Error occurred: {context}", exc_info=True)

def safe_json_response(data: Any, status_code: int = 200) -> JSONResponse:
    """Cria resposta JSON segura, tratando erros de serialização"""
    try:
        return JSONResponse(content=data, status_code=status_code)
    except Exception as e:
        logger.error(f"Failed to create JSON response: {str(e)}")
        return create_error_response(
            message="Failed to create response",
            status_code=500,
            error_code="SERIALIZATION_ERROR"
        )
