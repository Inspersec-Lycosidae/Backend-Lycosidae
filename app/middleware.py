"""
Middleware simplificado para validação de requests
"""
from fastapi import Request
from typing import Dict, Any
import re

try:
    from .logger import get_logger
    from .security import SecurityUtils
    from .exceptions import ValidationException
except ImportError:
    from logger import get_logger
    from security import SecurityUtils
    from exceptions import ValidationException

logger = get_logger(__name__)

def validate_request_headers(request: Request) -> bool:
    user_agent = request.headers.get("User-Agent", "")
    
    blocked_bots = [
        "bot", "crawler", "spider", "scraper",
        "scanner", "probe", "test"
    ]
    
    user_agent_lower = user_agent.lower()
    for bot in blocked_bots:
        if bot in user_agent_lower:
            logger.warning(f"Blocked bot request: {user_agent}")
            return False
    
    return True

def sanitize_request_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: sanitize_request_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_request_data(item) for item in data]
    elif isinstance(data, str):
        return SecurityUtils.sanitize_input(data)
    else:
        return data