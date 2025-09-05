"""
Aplicação principal FastAPI
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

try:
    from .routers import main_router, system_router_main
    from .logger import setup_logging
    from .config import settings, validate_settings
    from .exceptions import setup_exception_handlers
except ImportError:
    from routers import main_router, system_router_main
    from logger import setup_logging
    from config import settings, validate_settings
    from exceptions import setup_exception_handlers

logger = setup_logging()

try:
    validate_settings()
    logger.info("Configuration validation successful")
except ValueError as e:
    logger.error(f"Configuration validation failed: {str(e)}")
    raise

app = FastAPI(
    title="Backend-Lycosidae API",
    version=settings.app_version,
    description="API segura para o projeto Lycosidae com autenticação JWT e rate limiting",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None
)
logger.info("FastAPI application created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)
logger.info("CORS middleware configured")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts_list
)
logger.info("TrustedHost middleware configured")

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    # Remove o header Server se existir
    if "Server" in response.headers:
        del response.headers["Server"]
    
    return response

@app.get("/")
def read_root():
    return {"message": "Backend-Lycosidae API is running"}

app.include_router(main_router)
app.include_router(system_router_main)
logger.info("Routers included in application")

setup_exception_handlers(app)
logger.info("Exception handlers configured")

if __name__ == "__main__":
    logger.info("Starting backend-lycosidae")
    logger.info("Server will be available at http://0.0.0.0:8000")
    logger.info("API documentation available at http://0.0.0.0:8000/docs")
    
    import sys
    import os
    
    if os.path.basename(os.getcwd()) == 'app':
        logger.info("Running from app directory - using relative import")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        logger.info("Running from root directory - using absolute import")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
