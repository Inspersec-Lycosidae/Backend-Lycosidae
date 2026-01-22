from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import asyncio

from app.schemas.competition import CompetitionCreateDTO, CompetitionReadDTO, CompetitionUpdateDTO, CompetitionJoinDTO
from app.schemas.exercise import ExerciseReadDTO, ExerciseStudentReadDTO
from app.schemas.attendance import AttendanceCreateDTO #
from app.schemas.user import UserBase
from app.schemas.auth import AuthToken
from app.middleware import get_current_user #
from app.services.interpreter_client import interpreter #
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["competitions"])

@router.get("/", response_model=List[CompetitionReadDTO])
async def list_competitions(user: AuthToken = Depends(get_current_user)):
    """
    Lista as competições.
    - Admin: Vê todas.
    - Aluno: Vê apenas aquelas em que está inscrito.
    """
    all_competitions = await interpreter.list_competitions()

    if user.role == "admin":
        return all_competitions

    async def check_participation(comp):
        try:
            participants = await interpreter.get_competition_participants(comp['id'])
            if any(p['id'] == user.id for p in participants):
                return comp
        except Exception as e:
            logger.error(f"Erro ao verificar participação na competição {comp['id']}: {e}")
        return None

    tasks = [check_participation(comp) for comp in all_competitions]
    results = await asyncio.gather(*tasks)

    my_competitions = [r for r in results if r is not None]

    return my_competitions

@router.get("/{comp_id}", response_model=CompetitionReadDTO)
async def get_competition(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """Detalhes de uma competição específica."""
    comp = await interpreter.get_competition(comp_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Competição não encontrada")
    return comp

@router.get("/{comp_id}/participants", response_model=List[UserBase])
async def list_competition_participants(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """Lista os participantes inscritos nesta competição."""
    return await interpreter.get_competition_participants(comp_id)

@router.get("/{comp_id}/exercises", response_model=List[ExerciseStudentReadDTO])
async def list_competition_exercises(comp_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Retorna os exercícios da competição com a URL de conexão se o admin tiver feito o deploy.
    """

    if user.role != "admin":
        participants = await interpreter.get_competition_participants(comp_id)
        if not any(p["id"] == user.id for p in participants):
            raise HTTPException(status_code=403, detail="Você deve entrar na competição primeiro")

    exercises = await interpreter.get_competition_exercises(comp_id)
    all_containers = await interpreter.list_containers()
    
    active_map = {
        c["exercises_id"]: c["connection"] 
        for c in all_containers 
        if c.get("is_active")
    }
    
    for ex in exercises:
        ex["connection"] = active_map.get(ex["id"], "")
        
    return exercises

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
    Valida o invite_code, registra o usuário na competição e grava a presença automaticamente.
    """
    try:
        # 1. Buscamos a competição pelo invite_code para obter o ID real
        # O Interpreter /join retorna apenas uma mensagem, por isso resolvemos o ID manualmente aqui.
        all_competitions = await interpreter.list_competitions()
        target_comp = next((c for c in all_competitions if c.get("invite_code") == payload.invite_code), None)
        
        if not target_comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Código de convite inválido ou competição não encontrada."
            )

        # 2. Faz o registro do usuário na competição
        await interpreter.join_competition(payload, user.id)
        
        # 3. Registra a presença (Attendance) automaticamente usando o ID encontrado
        attendance_payload = AttendanceCreateDTO(competitions_id=target_comp["id"])
        await interpreter.record_attendance(attendance_payload, user.id)
        
        logger.info(f"Usuário {user.username} entrou na competição {target_comp['id']} (Attendance registrada)")
        return {"message": "Inscrição confirmada e presença registrada com sucesso!"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro no join_competition: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar sua inscrição."
        )

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