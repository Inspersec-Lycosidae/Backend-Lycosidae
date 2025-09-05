"""
Gerenciamento de senhas e tokens de segurança
"""
import secrets
import string
import re
from typing import Dict, Any
from passlib.context import CryptContext

try:
    from ..config import settings
    from ..logger import get_logger
except ImportError:
    from config import settings
    from logger import get_logger

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordManager:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_reset_token() -> str:
        return PasswordManager.generate_secure_token(64)
    
    @staticmethod
    def generate_verification_token() -> str:
        return PasswordManager.generate_secure_token(64)
    
    @staticmethod
    def generate_csrf_token() -> str:
        return PasswordManager.generate_secure_token(32)
    
    @staticmethod
    def verify_csrf_token(token: str, session_token: str) -> bool:
        return len(token) == 32 and token.isalnum()
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        result = {
            "is_valid": True,
            "errors": [],
            "score": 0
        }
        
        if len(password) < settings.password_min_length:
            result["errors"].append(f"Password must be at least {settings.password_min_length} characters long")
            result["is_valid"] = False
        
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
