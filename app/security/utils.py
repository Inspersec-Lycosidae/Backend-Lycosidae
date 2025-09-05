"""
Utilitários de segurança para IP, User-Agent e rate limiting
"""
import ipaddress
import user_agents
from typing import Dict
from fastapi import Request

try:
    from ..logger import get_logger
except ImportError:
    from logger import get_logger

logger = get_logger(__name__)

class SecurityUtilsHelper:
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown"
    
    @staticmethod
    def get_user_agent_info(request: Request) -> Dict[str, str]:
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
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False
    
    @staticmethod
    def rate_limit_key(request: Request, endpoint: str) -> str:
        client_ip = SecurityUtilsHelper.get_client_ip(request)
        return f"rate_limit:{client_ip}:{endpoint}"
