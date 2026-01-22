from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.schemas.container import ContainerReadDTO, ContainerInternalDTO
from app.schemas.auth import AuthToken
from app.middleware import get_current_user
from app.services.interpreter_client import interpreter
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["containers"])

@router.get("/", response_model=List[ContainerReadDTO])
async def list_all_containers(user: AuthToken = Depends(get_current_user)):
    """
    Lista todos os registros de containers no sistema.
    """
    if user.role != "admin":
        logger.warning(f"Usuário {user.username} tentou listar containers sem permissão.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado: Requer privilégios de administrador"
        )
    
    return await interpreter.list_all_containers()

@router.get("/{container_id}", response_model=ContainerReadDTO)
async def get_container_details(container_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Busca detalhes de um container específico.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    return await interpreter.get_container(container_id)

@router.get("/exercise/{ex_id}", response_model=ContainerReadDTO)
async def get_container_by_exercise(ex_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Retorna os dados de conexão para o exercício (IP/Porta).
    Acessível por qualquer utilizador logado para permitir o jogo.
    """
    container = await interpreter.get_container_by_exercise(ex_id)
    if not container:
        raise HTTPException(status_code=404, detail="Nenhum container ativo para este exercício")
    return container

@router.post("/", response_model=ContainerReadDTO, status_code=201)
async def register_container(payload: ContainerInternalDTO, exercises_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Registra um novo container vinculado a um exercício.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem registrar novos containers")
    
    logger.info(f"Admin {user.username} registrando container para o exercício {exercises_id}")
    return await interpreter.create_container(payload, exercises_id)

@router.delete("/{container_id}", status_code=204)
async def remove_container(container_id: str, user: AuthToken = Depends(get_current_user)):
    """
    Remove o registro de um container e interrompe sua disponibilidade.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Operação não permitida")
    
    logger.info(f"Admin {user.username} removendo container {container_id}")
    return await interpreter.remove_container(container_id)