"""
Aplicação principal FastAPI
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

try:
    # Imports relativos quando executado como módulo
    from .routers import router
    from .logger import setup_logging
    from .config import settings, validate_settings
    from .exceptions import setup_exception_handlers
except ImportError:
    # Imports absolutos quando executado diretamente
    from routers import router
    from logger import setup_logging
    from config import settings, validate_settings
    from exceptions import setup_exception_handlers

logger = setup_logging()

# Valida configurações críticas
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

# Configuração de CORS segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)
logger.info("CORS middleware configured")

# Middleware de hosts confiáveis
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)
logger.info("TrustedHost middleware configured")

# Middleware básico de segurança
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Middleware de segurança básico"""
    response = await call_next(request)
    
    # Headers de segurança básicos
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers.pop("Server", None)
    
    return response

# Endpoint adicional para a raiz (/) conforme especificação
@app.get("/")
def read_root():
    """Read Root"""
    return {"message": "Backend-Lycosidae API is running"}

# Inclui routers
app.include_router(router)
logger.info("Router included in application")

# Configura handlers de exceção
setup_exception_handlers(app)
logger.info("Exception handlers configured")

if __name__ == "__main__":
    logger.info("Starting backend-lycosidae")
    logger.info("Server will be available at http://0.0.0.0:8000")
    logger.info("API documentation available at http://0.0.0.0:8000/docs")
    
    # Detectar se está sendo executado de dentro da pasta app ou da raiz
    import sys
    import os
    
    # Se estiver na pasta app, usar import relativo
    if os.path.basename(os.getcwd()) == 'app':
        logger.info("Running from app directory - using relative import")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        # Se estiver na raiz, usar import absoluto
        logger.info("Running from root directory - using absolute import")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)




