from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.schemas.team import ScoreboardEntryDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["scoreboard"])

@router.get("/{comp_id}", response_model=List[ScoreboardEntryDTO])
async def get_competition_scoreboard(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Retorna o placar de uma competição específica ordenado por pontuação.
    
    Regras de Negócio:
    1. Administradores podem visualizar qualquer placar.
    2. Alunos só podem visualizar o placar de competições onde possuem presença (Attendance) registrada.
    """
    
    # 1. Validação de Acesso para Alunos
    if user.role != "admin":
        attendance = await interpreter.get_user_attendance(user.id)
        is_registered = any(a["competitions_id"] == comp_id for a in attendance)
        
        if not is_registered:
            logger.warning(f"Usuário {user.username} tentou acessar o scoreboard da competição {comp_id} sem estar inscrito.")
            raise HTTPException(status_code=403, detail="Você precisa estar inscrito nesta aula/competição para ver o placar.")

    logger.info(f"Usuário {user.username} acessando scoreboard da competição {comp_id}")
    
    return await interpreter.get_scoreboard(comp_id)