"""
Sistema de Rate Limiting simplificado
"""
import time
import asyncio
import functools
from typing import Dict
from fastapi import Request, HTTPException

try:
    from .config import settings
    from .logger import get_logger
except ImportError:
    from config import settings
    from logger import get_logger

logger = get_logger(__name__)

class SimpleRateLimiter:
    """Sistema de rate limiting simples em memória"""
    
    def __init__(self):
        self.requests: Dict[str, Dict] = {}
    
    def is_allowed(self, identifier: str, limit: int = 100, window: int = 60) -> bool:
        """Verifica se a requisição é permitida"""
        current_time = time.time()
        
        # Limpa entradas antigas
        self._cleanup_old_entries(current_time, window)
        
        # Verifica limite para este identificador
        if identifier not in self.requests:
            self.requests[identifier] = {'count': 0, 'reset_time': current_time + window}
        
        entry = self.requests[identifier]
        
        # Reset se a janela expirou
        if current_time > entry['reset_time']:
            entry['count'] = 0
            entry['reset_time'] = current_time + window
        
        # Verifica se excedeu o limite
        if entry['count'] >= limit:
            return False
        
        entry['count'] += 1
        return True
    
    def _cleanup_old_entries(self, current_time: float, window: int):
        """Remove entradas antigas"""
        expired_keys = [
            key for key, data in self.requests.items() 
            if current_time > data['reset_time'] + window
        ]
        for key in expired_keys:
            del self.requests[key]

# Instância global
limiter = SimpleRateLimiter()

def rate_limit_middleware(endpoint: str, requests_per_minute: int = 60):
    """Decorator para rate limiting"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontra o Request nos argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # Se não há Request, pula o rate limiting
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Identifica o cliente
            client_ip = request.client.host if request.client else "unknown"
            identifier = f"{client_ip}:{endpoint}"
            
            # Verifica rate limit
            if not limiter.is_allowed(identifier, requests_per_minute, 60):
                logger.warning(f"Rate limit exceeded for {identifier}")
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": "60"}
                )
            
            # Executa a função
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

def get_rate_limit_info(request: Request) -> Dict:
    """Retorna informações sobre rate limiting"""
    client_ip = request.client.host if request.client else "unknown"
    
    return {
        "limit": settings.rate_limit_requests,
        "window": settings.rate_limit_window,
        "client_ip": client_ip,
        "message": "Rate limiting is active"
    }