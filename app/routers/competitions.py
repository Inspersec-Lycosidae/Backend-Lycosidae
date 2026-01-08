from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime, timezone

from app.schemas.competition import CompetitionCreateDTO, CompetitionReadDTO, CompetitionUpdateDTO, CompetitionJoinDTO
from app.schemas.exercise import ExerciseReadDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["competitions"])

@router.get("/", response_model=List[CompetitionReadDTO])
async def list_competitions():
    """Lista todas as competições disponíveis"""
    return await interpreter.list_competitions()

@router.get("/{comp_id}", response_model=CompetitionReadDTO)
async def get_competition(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """Detalhes de uma competição específica."""
    comp = await interpreter.get_competition(comp_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Competição não encontrada")
    return comp

@router.get("/{comp_id}/participants", response_model=List[CompetitionReadDTO])
async def list_competition_participants(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """Lista os participantes inscritos nesta competição."""
    return await interpreter.get_competition_participants(comp_id)

@router.get("/{comp_id}/exercises", response_model=List[ExerciseReadDTO])
async def list_competition_exercises(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Lista os exercícios apenas se o aluno:
    1. Tiver registrado presença (Attendance).
    2. Estiver em um time vinculado a esta competição.
    """

    if user.role == "admin":
        return await interpreter.get_competition_exercises(comp_id)

    # 1. Verificar Presença
    attendance = await interpreter.get_user_attendance(user.id)
    if not any(a["competitions_id"] == comp_id for a in attendance):
        raise HTTPException(status_code=403, detail="Você deve entrar na competição primeiro")

    logger.info(f"Usuário {user.username} acessando exercícios da competição {comp_id}")
    return await interpreter.get_competition_exercises(comp_id)

@router.post("/", response_model=CompetitionReadDTO, status_code=201)
async def create_competition(payload: CompetitionCreateDTO, user: AuthToken = Depends(get_current_user)):
    """Apenas administradores podem criar novas competições/aulas."""
    if user.role != "admin":
        logger.warning(f"Usuário {user.username} tentou criar competição sem permissão.")
        raise HTTPException(status_code=403, detail="Acesso negado: Requer privilégios de administrador")

    return await interpreter.create_competition(payload)

@router.post("/join")
async def join_competition(payload: CompetitionJoinDTO, user: AuthToken = Depends(get_current_user)):
    """
    Valida o invite_code e registra a presença (Attendance).
    """
    comp = await interpreter.get_competition(comp_id)
    if not comp or comp["invite_code"] != payload.invite_code:
        raise HTTPException(status_code=400, detail="Código de convite inválido")

    attendance_data = {"users_id": user.id, "competitions_id": comp_id}
    await interpreter.record_attendance(attendance_data)

    logger.info(f"Usuário {user.username} entrou com sucesso na competição {comp_id}")
    return {"message": "Inscrição confirmada. Agora você pode criar um novo time ou entrar em um time existente."}

@router.patch("/{comp_id}", response_model=CompetitionReadDTO)
async def update_competition(comp_id: str, payload: CompetitionUpdateDTO, user: AuthToken = Depends(get_current_user)):
    """Atualiza dados da competição (Apenas Admin)."""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return await interpreter.update_competition(comp_id, payload)

@router.delete("/{comp_id}", status_code=204)
async def delete_competition(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """Remove uma competição (Apenas Admin)."""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return await interpreter.delete_competition(comp_id)