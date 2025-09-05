"""
Módulo core com dependências centrais
"""

from .dependencies import (
    get_token,
    verify_token_dependency,
    get_current_user,
    get_admin_user,
    get_rate_limiter,
    get_interpreter_client,
    get_request_info,
    get_logger_context,
    require_permission,
    require_owner_or_admin
)

__all__ = [
    "get_token",
    "verify_token_dependency", 
    "get_current_user",
    "get_admin_user",
    "get_rate_limiter",
    "get_interpreter_client",
    "get_request_info",
    "get_logger_context",
    "require_permission",
    "require_owner_or_admin"
]
