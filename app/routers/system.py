"""
Rotas do sistema (health check, rate limit, etc.)
"""
from fastapi import APIRouter, Request, Depends
from datetime import datetime
import time

try:
    from ..schemas import HealthCheckDTO, RateLimitInfoDTO
    from ..logger import get_logger
    from ..config import settings
    from ..rate_limiter import rate_limit_middleware, get_rate_limit_info
    from ..interpreter_client import InterpreterClient
except ImportError:
    from schemas import HealthCheckDTO, RateLimitInfoDTO
    from logger import get_logger
    from config import settings
    from rate_limiter import rate_limit_middleware, get_rate_limit_info
    from interpreter_client import InterpreterClient

logger = get_logger(__name__)
router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health", 
           description="Health check endpoint",
           response_model=HealthCheckDTO,
           summary="Health Check")
@rate_limit_middleware("health_check", 60)
async def health_check(request: Request):
    logger.info("Health check endpoint accessed")
    
    interpreter_status = "unknown"
    try:
        async with InterpreterClient() as client:
            result = await client.health_check()
            interpreter_status = "success" if result.get("status") == "healthy" else "error"
    except Exception as e:
        logger.warning(f"Interpreter health check failed: {str(e)}")
        interpreter_status = "error"
    
    health_data = HealthCheckDTO(
        status="healthy" if interpreter_status == "success" else "degraded",
        message="Backend is running properly" if interpreter_status == "success" else "Backend running with issues",
        service=settings.app_name,
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        database_status=interpreter_status
    )
    
    return health_data

@router.get("/rate-limit/info", 
           description="Get rate limit information",
           response_model=RateLimitInfoDTO,
           summary="Rate Limit Info")
def get_rate_limit_status(request: Request):
    rate_info = get_rate_limit_info(request, "rate_limit_info")
    
    return RateLimitInfoDTO(
        limit=rate_info["limit"],
        remaining=rate_info["remaining"],
        reset_time=rate_info["reset_time"],
        retry_after=max(0, rate_info["reset_time"] - int(time.time()))
    )
