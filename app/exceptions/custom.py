"""
Exceções personalizadas da API
"""
from typing import Dict, Any, Optional

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
