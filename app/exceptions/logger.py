"""
Logger especializado para exceções
"""
from typing import Dict, Any, Optional
from fastapi import Request

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

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
