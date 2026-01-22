from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.attendance import AttendanceReadDTO, AttendanceCreateDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter

router = APIRouter(tags=["attendance"])

@router.post("/", response_model=AttendanceReadDTO, status_code=201)
async def record_attendance(payload: AttendanceCreateDTO, user: AuthToken = Depends(get_current_user)):
    """
    Regista a presença de um utilizador numa competição.
    Regra: Jogadores só podem registar a própria presença. Admins podem registar para qualquer um.
    """
    is_admin = user.role == "admin"
    is_self = payload.users_id == user.id

    if not is_admin and not is_self:
        raise HTTPException(
            status_code=403, 
            detail="Não tem permissão para registar presença para outro utilizador."
        )
    
    return await interpreter.record_attendance(payload)

@router.get("/user/{user_id}", response_model=List[AttendanceReadDTO])
async def get_user_attendance(user_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Retorna o histórico de presenças de um utilizador específico.
    Regra: Utilizadores comuns só podem ver o seu próprio histórico.
    """
    is_admin = user.role == "admin"
    is_self = user_id == user.id

    if not is_admin and not is_self:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado ao histórico de presenças de terceiros."
        )

    return await interpreter.get_user_attendance(user_id)