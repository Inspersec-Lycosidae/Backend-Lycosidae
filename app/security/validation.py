"""
Validadores de entrada e dados
"""
import re
from typing import Dict, Any

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

class InputValidator:
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Any]:
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
        
        forbidden_usernames = ['admin', 'root', 'administrator', 'system', 'api', 'www', 'mail', 'ftp']
        if username.lower() in forbidden_usernames:
            result["errors"].append("Username not allowed")
            result["is_valid"] = False
        
        return result
    
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_email_domain(email: str) -> bool:
        disposable_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        ]
        
        domain = email.split('@')[1].lower()
        return domain not in disposable_domains
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        if not isinstance(input_string, str):
            return str(input_string)
        
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_string)
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        sanitized = sanitized.replace('\\', '\\\\')
        sanitized = sanitized.replace("'", "\\'")
        sanitized = sanitized.replace('"', '\\"')
        
        return sanitized.strip()
