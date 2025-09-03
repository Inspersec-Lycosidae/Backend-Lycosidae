# database.py
import os
import dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
try:
    from .logger import get_logger
except ImportError:
    from logger import get_logger

# Configuração do logger para este módulo
logger = get_logger(__name__)

# Carregar variáveis de ambiente
dotenv.load_dotenv()

def test_database_connection():
    """
    Função para testar a conexão com o banco de dados.
    Retorna um dicionário com informações sobre o status da conexão.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        return {
            "status": "error",
            "message": "Variável de ambiente DATABASE_URL não configurada",
            "error_type": "ConfigurationError"
        }
    
    try:
        # Criar engine temporário para teste
        engine = create_engine(DATABASE_URL, echo=False)
        
        # Testar conexão com uma query simples
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            test_value = result.fetchone()[0]
        
        logger.info("Database connection test successful")
        return {
            "status": "success",
            "message": "Conexão com o banco de dados estabelecida com sucesso",
            "test_query_result": test_value
        }
            
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Erro de conexão com o banco de dados: {str(e)}",
            "error_type": "SQLAlchemyError"
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Erro inesperado: {str(e)}",
            "error_type": "UnexpectedError"
        }
