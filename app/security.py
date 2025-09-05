"""
Sistema de segurança e utilitários
"""
import hashlib
import secrets
import string
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import ipaddress
import user_agents

try:
    from .config import settings
    from .logger import get_logger
except ImportError:
    from config import settings
    from logger import get_logger

logger = get_logger(__name__)

# Configuração de hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração de autenticação HTTP Bearer
security = HTTPBearer()

class SecurityUtils:
    """Utilitários de segurança"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de senha usando bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica senha usando bcrypt"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Gera token seguro aleatório"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_reset_token() -> str:
        """Gera token de reset de senha"""
        return SecurityUtils.generate_secure_token(64)
    
    @staticmethod
    def generate_verification_token() -> str:
        """Gera token de verificação de email"""
        return SecurityUtils.generate_secure_token(64)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT de acesso"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expiration)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT de refresh"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)  # Refresh token válido por 7 dias
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            
            # Verifica tipo do token
            if payload.get("type") != token_type:
                raise HTTPException(status_code=401, detail=f"Invalid token type. Expected {token_type}")
            
            # Verifica expiração
            exp = payload.get("exp")
            if exp is None or datetime.utcnow().timestamp() > exp:
                raise HTTPException(status_code=401, detail="Token expired")
            
            return payload
        except JWTError as e:
            logger.warning(f"JWT verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitiza entrada do usuário"""
        if not isinstance(input_string, str):
            return str(input_string)
        
        # Remove caracteres de controle e caracteres perigosos
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_string)
        
        # Remove tags HTML/XML
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        
        # Remove caracteres de escape perigosos
        sanitized = sanitized.replace('\\', '\\\\')
        sanitized = sanitized.replace("'", "\\'")
        sanitized = sanitized.replace('"', '\\"')
        
        return sanitized.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Valida força da senha"""
        result = {
            "is_valid": True,
            "errors": [],
            "score": 0
        }
        
        # Comprimento mínimo
        if len(password) < settings.password_min_length:
            result["errors"].append(f"Password must be at least {settings.password_min_length} characters long")
            result["is_valid"] = False
        
        # Verificações de complexidade
        if settings.password_require_uppercase and not re.search(r'[A-Z]', password):
            result["errors"].append("Password must contain at least one uppercase letter")
            result["is_valid"] = False
        
        if settings.password_require_lowercase and not re.search(r'[a-z]', password):
            result["errors"].append("Password must contain at least one lowercase letter")
            result["is_valid"] = False
        
        if settings.password_require_numbers and not re.search(r'\d', password):
            result["errors"].append("Password must contain at least one number")
            result["is_valid"] = False
        
        if settings.password_require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result["errors"].append("Password must contain at least one special character")
            result["is_valid"] = False
        
        # Calcula score de força
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        if len(password) >= 12:
            score += 1
        
        result["score"] = score
        return result
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """Obtém IP do cliente considerando proxies"""
        # Verifica headers de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Pega o primeiro IP da lista
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # IP direto
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown"
    
    @staticmethod
    def get_user_agent_info(request: Request) -> Dict[str, str]:
        """Extrai informações do User-Agent"""
        user_agent_string = request.headers.get("User-Agent", "")
        if not user_agent_string:
            return {
                "browser": "Unknown",
                "os": "Unknown",
                "device": "Unknown",
                "raw": ""
            }
        
        try:
            ua = user_agents.parse(user_agent_string)
            return {
                "browser": ua.browser.family if ua.browser else "Unknown",
                "os": ua.os.family if ua.os else "Unknown",
                "device": ua.device.family if ua.device else "Unknown",
                "raw": user_agent_string
            }
        except Exception as e:
            logger.warning(f"Failed to parse user agent: {str(e)}")
            return {
                "browser": "Unknown",
                "os": "Unknown",
                "device": "Unknown",
                "raw": user_agent_string
            }
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Verifica se IP é válido"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """Verifica se IP é privado"""
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False
    
    @staticmethod
    def rate_limit_key(request: Request, endpoint: str) -> str:
        """Gera chave para rate limiting"""
        client_ip = SecurityUtils.get_client_ip(request)
        return f"rate_limit:{client_ip}:{endpoint}"
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Gera token CSRF"""
        return SecurityUtils.generate_secure_token(32)
    
    @staticmethod
    def verify_csrf_token(token: str, session_token: str) -> bool:
        """Verifica token CSRF"""
        # Implementação básica - em produção usar HMAC
        return len(token) == 32 and token.isalnum()

class InputValidator:
    """Validador de entradas"""
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Any]:
        """Valida username"""
        result = {"is_valid": True, "errors": []}
        
        if not username:
            result["errors"].append("Username is required")
            result["is_valid"] = False
            return result
        
        if len(username) < 3:
            result["errors"].append("Username must be at least 3 characters long")
            result["is_valid"] = False
        
        if len(username) > 50:
            result["errors"].append("Username must be at most 50 characters long")
            result["is_valid"] = False
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            result["errors"].append("Username must contain only letters, numbers, underscores, and hyphens")
            result["is_valid"] = False
        
        # Usernames proibidos
        forbidden_usernames = ['admin', 'root', 'administrator', 'system', 'api', 'www', 'mail', 'ftp']
        if username.lower() in forbidden_usernames:
            result["errors"].append("Username not allowed")
            result["is_valid"] = False
        
        return result
    
    @staticmethod
    def validate_email_domain(email: str) -> bool:
        """Valida domínio do email"""
        # Lista de domínios temporários/descartáveis conhecidos
        disposable_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        ]
        
        domain = email.split('@')[1].lower()
        return domain not in disposable_domains
