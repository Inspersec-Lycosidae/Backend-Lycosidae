#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    # Imports relativos quando executado como módulo
    from .routers import router
    from .logger import setup_logging
except ImportError:
    # Imports absolutos quando executado diretamente
    from routers import router
    from logger import setup_logging
import uvicorn

logger = setup_logging()


app = FastAPI(
    title="Swagger das API do projeto Lycosidade ",
    version="1.0.0"
)
logger.info("FastAPI application created")

app.include_router(router)
logger.info("Router included in application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
logger.info("CORS middleware configured")

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




