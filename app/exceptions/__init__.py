"""
Sistema de exceções modularizado
"""

from .custom import (
    BaseAPIException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    NotFoundException,
    ConflictException,
    RateLimitException,
    DatabaseException,
    ExternalServiceException,
    BusinessLogicException
)
from .handlers import setup_exception_handlers
from .responses import create_error_response, safe_json_response
from .logger import ErrorLogger

__all__ = [
    # Custom exceptions
    "BaseAPIException",
    "ValidationException",
    "AuthenticationException", 
    "AuthorizationException",
    "NotFoundException",
    "ConflictException",
    "RateLimitException",
    "DatabaseException",
    "ExternalServiceException",
    "BusinessLogicException",
    # Setup function
    "setup_exception_handlers",
    # Response utilities
    "create_error_response",
    "safe_json_response",
    # Error logging
    "ErrorLogger"
]
