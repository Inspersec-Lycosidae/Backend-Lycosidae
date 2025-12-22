from typing import List
from fastapi import APIRouter, HTTPException, Depends, status

from app.schemas.team import TeamReadDTO, TeamCreateDTO, JoinTeamDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["teams"])

@router.get("/{team_id}", response_model=TeamReadDTO)
async def get_team(team_id: str, user: AuthToken = Depends(get_current_user)):
    """Ver detalhes de um time específico."""
    team = await interpreter.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return team

@router.post("/competition/{comp_id}", response_model=TeamReadDTO, status_code=201)
async def create_team(comp_id: str, payload: TeamCreateDTO, user: AuthToken = Depends(get_current_user)):
    """
    Cria um time vinculado a uma competição.
    Regras:
    1. O usuário deve estar inscrito na competição (Attendance).
    2. O usuário não pode já pertencer a outro time nesta mesma competição.
    """
    attendance = await interpreter.get_user_attendance(user.id)
    if not any(a["competitions_id"] == comp_id for a in attendance):
        raise HTTPException(status_code=403, detail="Você precisa entrar na competição (usar o código de convite) antes de criar um time.")

    teams = await interpreter.get_competition_teams(comp_id)
    if any(user.id in t.get("members_ids", []) for t in teams):
        raise HTTPException(status_code=400, detail="Você já faz parte de um time nesta competição.")

    if not payload.creator_id:
        payload.creator_id = user.id
        
    logger.info(f"Usuário {user.username} criando o time '{payload.name}' para a competição {comp_id}")
    return await interpreter.create_team(comp_id, payload)

@router.post("/{team_id}/join")
async def join_team(team_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Entra em um time existente.
    Regras:
    1. O usuário deve estar inscrito na competição do time.
    2. O usuário não pode já estar em outro time da mesma competição.
    """
    team = await interpreter.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    # Busca todas as presenças do usuário
    attendance = await interpreter.get_user_attendance(user.id)
    
    join_data = JoinTeamDTO(users_id=user.id)
    logger.info(f"Usuário {user.username} tentando entrar no time {team_id}")
    return await interpreter.join_team(team_id, join_data)

@router.delete("/{team_id}/leave")
async def leave_team_self(team_id: str, user: AuthToken = Depends(get_current_user)):
    """O próprio usuário decide sair do time."""
    logger.info(f"Usuário {user.username} saindo do time {team_id}")
    return await interpreter.leave_team(team_id, user.id)

@router.delete("/{team_id}/kick/{target_user_id}")
async def kick_member(team_id: str, target_user_id: str, user: AuthToken = Depends(get_current_user)):
    """Remove um membro (Apenas Admin ou Criador do Time)."""
    team = await interpreter.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")

    # Validação de permissão: Admin ou o dono do time
    is_admin = user.role == "admin"
    is_creator = team.get("creator_id") == user.id

    if not is_admin and not is_creator:
        logger.warning(f"Usuário {user.username} tentou expulsar membro do time {team_id} sem permissão.")
        raise HTTPException(status_code=403, detail="Você não tem permissão para remover membros deste time.")

    return await interpreter.leave_team(team_id, target_user_id)