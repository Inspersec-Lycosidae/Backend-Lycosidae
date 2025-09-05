"""
Utilitários para respostas de erro
"""
from typing import Dict, Any, Optional
from fastapi.responses import JSONResponse

try:
    from ..schemas.system import ErrorResponseDTO
    from ..logger import get_logger
except ImportError:
    from schemas.system import ErrorResponseDTO
    from logger import get_logger

logger = get_logger(__name__)

def create_error_response(
    message: str,
    status_code: int = 500,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """Cria resposta de erro padronizada"""
    error_response = ErrorResponseDTO(
        error=message,
        detail=error_code or "UNKNOWN_ERROR",
        code=error_code
    )
    
    # Adiciona detalhes se fornecidos
    if details:
        error_data = error_response.dict()
        error_data["details"] = details
        return JSONResponse(
            status_code=status_code,
            content=error_data
        )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict()
    )

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
