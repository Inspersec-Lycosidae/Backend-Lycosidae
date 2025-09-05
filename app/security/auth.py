"""
Sistema de autenticação JWT
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer

try:
    from ..config import settings
    from ..logger import get_logger
except ImportError:
    from config import settings
    from logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()

class SecurityUtils:
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
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
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            
            if payload.get("type") != token_type:
                raise HTTPException(status_code=401, detail=f"Invalid token type. Expected {token_type}")
            
            exp = payload.get("exp")
            if exp is None or datetime.utcnow().timestamp() > exp:
                raise HTTPException(status_code=401, detail="Token expired")
            
            return payload
        except JWTError as e:
            logger.warning(f"JWT verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
