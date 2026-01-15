from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List

from app.schemas.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.schemas.auth import LoginPayload, AuthToken
from app.utils import pass_hasher
from app.middleware import make_cookie_from_model, get_current_user
from app.logger import get_logger
from app.services.interpreter_client import interpreter

logger = get_logger(__name__)
router = APIRouter(tags=["auth"])

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,
    "samesite": "lax",
    "max_age": 3600,
}

@router.get("/me", response_model=UserReadDTO)
async def read_me(current_user: AuthToken = Depends(get_current_user)):
    """
    Retorna os dados do utilizador logado.
    """
    user_data = await interpreter.get_user_by_id(current_user.id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return UserReadDTO(**user_data)

@router.get("/users", response_model=List[UserReadDTO])
async def list_all_users(user: AuthToken = Depends(get_current_user)):
    """
    Lista todos os alunos registados no sistema.
    """
    if user.role != "admin":
        logger.warning(f"Utilizador {user.username} tentou listar alunos sem permissão.")
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores")
    
    return await interpreter.list_users()

@router.post("/register", response_model=UserReadDTO, status_code=201)
async def register(payload: UserCreateDTO):
    """
    Proxy para o Interpreter. 
    """

    return await interpreter.register_user(payload)

@router.post("/login")
async def login(payload: LoginPayload):
    """
    Fluxo de Login Híbrido:
    1. Busca hash no Interpreter por email.
    2. Valida hash localmente no Backend.
    3. Emite Cookie de sessão.
    """

    user_internal = await interpreter.get_user_internal(payload.email)
    
    if not user_internal:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    input_hash = pass_hasher(payload.password)
    if input_hash != user_internal["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token_payload = AuthToken(
        id=user_internal["id"],
        username=user_internal["username"],
        email=user_internal["email"],
        role="admin" if user_internal.get("is_admin") else "student"
    )
    
    token = make_cookie_from_model(token_payload)

    response = JSONResponse({"message": "Login successful", "user": user_internal["username"]})
    response.set_cookie("session_token", token, **COOKIE_SETTINGS)
    return response

@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logged out"})
    
    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=True, 
        samesite="lax"
    )
    return response

@router.put("/me", response_model=UserReadDTO)
async def update_my_profile(payload: UserUpdateDTO, current_user: AuthToken = Depends(get_current_user)):
    """
    Permite ao utilizador atualizar os seus próprios dados (nome, senha, etc).
    """
    return await interpreter.update_user(current_user.id, payload)