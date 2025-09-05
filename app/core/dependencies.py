"""
Sistema de dependency injection
"""
from typing import Optional
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

try:
    from ..security.auth import SecurityUtils
    from ..security.utils import SecurityUtilsHelper
    from ..rate_limiter import RateLimiter
    from ..interpreter_client import InterpreterClient
    from ..logger import get_logger
    from ..exceptions.custom import AuthenticationException, AuthorizationException
except ImportError:
    from security.auth import SecurityUtils
    from security.utils import SecurityUtilsHelper
    from rate_limiter import RateLimiter
    from interpreter_client import InterpreterClient
    from logger import get_logger
    from exceptions.custom import AuthenticationException, AuthorizationException

logger = get_logger(__name__)
security = HTTPBearer(auto_error=False)

# Dependency para obter token JWT
async def get_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """Extrai token JWT do header Authorization"""
    if not credentials:
        raise AuthenticationException("Missing authentication token")
    
    return credentials.credentials

# Dependency para verificar token
async def verify_token_dependency(token: str = Depends(get_token)) -> dict:
    """Verifica se o token JWT é válido"""
    try:
        payload = SecurityUtils.verify_token(token)
        return payload
    except HTTPException as e:
        raise AuthenticationException(e.detail)

# Dependency para obter usuário atual
async def get_current_user(payload: dict = Depends(verify_token_dependency)) -> dict:
    """Retorna informações do usuário atual"""
    return {
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "email": payload.get("email"),
        "permissions": payload.get("permissions", [])
    }

# Dependency para verificar se é admin
async def get_admin_user(user: dict = Depends(get_current_user)) -> dict:
    """Verifica se o usuário é admin"""
    if "admin" not in user.get("permissions", []):
        raise AuthorizationException("Admin privileges required")
    
    return user

# Dependency para rate limiter
def get_rate_limiter() -> RateLimiter:
    """Retorna instância do rate limiter"""
    return RateLimiter()

# Dependency para interpreter client
def get_interpreter_client() -> InterpreterClient:
    """Retorna instância do interpreter client"""
    return InterpreterClient()

# Dependency para informações do request
async def get_request_info(request: Request) -> dict:
    """Extrai informações do request"""
    return {
        "client_ip": SecurityUtilsHelper.get_client_ip(request),
        "user_agent": SecurityUtilsHelper.get_user_agent_info(request),
        "request_id": getattr(request.state, "request_id", None),
        "url": str(request.url),
        "method": request.method
    }

# Dependency para logs estruturados
async def get_logger_context(
    request_info: dict = Depends(get_request_info),
    user: Optional[dict] = None
) -> dict:
    """Cria contexto para logs estruturados"""
    context = {
        "request_info": request_info
    }
    
    if user:
        context["user"] = {
            "user_id": user.get("user_id"),
            "username": user.get("username")
        }
    
    return context

# Dependency para validar permissões específicas
def require_permission(permission: str):
    """Factory para criar dependency que valida permissão específica"""
    
    async def permission_checker(user: dict = Depends(get_current_user)) -> dict:
        user_permissions = user.get("permissions", [])
        
        if permission not in user_permissions and "admin" not in user_permissions:
            raise AuthorizationException(f"Permission '{permission}' required")
        
        return user
    
    return permission_checker

# Dependency para validar proprietário do recurso
def require_owner_or_admin(resource_user_id_key: str = "user_id"):
    """Factory para criar dependency que valida se usuário é dono do recurso ou admin"""
    
    async def owner_checker(
        resource_data: dict,
        user: dict = Depends(get_current_user)
    ) -> dict:
        resource_owner_id = resource_data.get(resource_user_id_key)
        current_user_id = user.get("user_id")
        is_admin = "admin" in user.get("permissions", [])
        
        if not is_admin and resource_owner_id != current_user_id:
            raise AuthorizationException("Access denied: not resource owner")
        
        return user
    
    return owner_checker
