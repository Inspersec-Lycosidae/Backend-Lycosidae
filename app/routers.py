# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas import *
from middleware import *
from logger import get_logger
from typing import Optional

# Configuração do logger para este módulo
logger = get_logger(__name__)

router = APIRouter(
    prefix="/",
    tags=["backend"]
)

###################################
##### Routers Functions Below #####
###################################


@router.get("/healthy", description="Health check endpoint")
def health_check():
    
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "message": "Backend is running properly",
        "service": "Backend-Lycosidae"
    }


