# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
try:
    # Imports relativos quando executado como módulo
    from .schemas import *
    from .middleware import *
    from .logger import get_logger
    from .database import test_database_connection
except ImportError:
    # Imports absolutos quando executado diretamente
    from schemas import *
    from middleware import *
    from logger import get_logger
    from database import test_database_connection
from typing import Optional

# Configuração do logger para este módulo
logger = get_logger(__name__)

router = APIRouter(
    prefix="/route",
    tags=["route"]
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


@router.get("/test-db", description="Test database connection endpoint")
def test_db_connection():
    """
    Endpoint para testar a conexão com o banco de dados.
    Retorna informações sobre o status da conexão.
    """
    logger.info("Database connection test endpoint accessed")
    
    try:
        # Testar a conexão com o banco de dados
        result = test_database_connection()
        
        # Se a conexão foi bem-sucedida, retornar status 200
        if result["status"] == "success":
            logger.info("Database connection test completed successfully")
            return JSONResponse(
                status_code=200,
                content=result
            )
        else:
            # Se houve erro na conexão, retornar status 500
            logger.error(f"Database connection test failed: {result['message']}")
            return JSONResponse(
                status_code=500,
                content=result
            )
            
    except Exception as e:
        # Capturar qualquer erro inesperado
        error_message = f"Erro inesperado ao testar conexão com banco de dados: {str(e)}"
        logger.error(error_message)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": error_message,
                "error_type": "UnexpectedError"
            }
        )