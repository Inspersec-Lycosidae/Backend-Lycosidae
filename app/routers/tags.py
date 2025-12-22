from typing import List
from fastapi import APIRouter, HTTPException, Depends, status

from app.schemas.tag import TagReadDTO, TagCreateDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["tags"])

@router.get("/", response_model=List[TagReadDTO])
async def list_tags():
    """
    Lista todas as tags de exercícios cadastradas no sistema.
    Acesso permitido para todos os usuários autenticados.
    """
    return await interpreter.list_tags()

@router.post("/", response_model=TagReadDTO, status_code=201)
async def create_tag(payload: TagCreateDTO, user: AuthToken = Depends(get_current_user)):
    """
    Cria uma nova tag para classificação de desafios CTF.
    """
    if user.role != "admin":
        logger.warning(f"Usuário {user.username} tentou criar tag sem permissão.")
        raise HTTPException(status_code=403, detail="Acesso negado: Requer privilégios de administrador")
    
    logger.info(f"Admin {user.username} criando nova tag: {payload.name}")
    return await interpreter.create_tag(payload)

@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Remove uma tag do sistema.
    """
    if user.role != "admin":
        logger.warning(f"Usuário {user.username} tentou deletar tag {tag_id} sem permissão.")
        raise HTTPException(status_code=403, detail="Operação não permitida")
    
    logger.info(f"Admin {user.username} deletando tag ID: {tag_id}")
    return await interpreter.delete_tag(tag_id)