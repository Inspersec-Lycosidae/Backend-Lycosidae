# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from app.logger import setup_logging
import uvicorn
import os

"""

Entry point for Backend-Lycosidae service.
Responsibilities:
  - Initialize FastAPI
  - Configure CORS
  - Include routers
  - Setup logging

"""

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
    logger.info("Starting Backend-Lycosidae")
    logger.info("Server will be available at http://0.0.0.0:8000")
    logger.info("API documentation available at http://0.0.0.0:8000/docs")
    
    
    # If on app folder, use relative import
    if os.path.basename(os.getcwd()) == 'app':
        logger.info("Running from app directory - using relative import")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        # If on root folder, use absolute import
        logger.info("Running from root directory - using absolute import")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
