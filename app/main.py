#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from logger import setup_logging
import uvicorn
import os

logger = setup_logging()


app = FastAPI()
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
    
    
    # Se estiver na pasta app, usar import relativo
    if os.path.basename(os.getcwd()) == 'app':
        logger.info("Running from app directory - using relative import")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        # Se estiver na raiz, usar import absoluto
        logger.info("Running from root directory - using absolute import")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)




