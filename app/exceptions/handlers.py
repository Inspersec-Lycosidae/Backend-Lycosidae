"""
Handlers de exceções
"""
import traceback
import os
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .custom import BaseAPIException
from .responses import create_error_response

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

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
