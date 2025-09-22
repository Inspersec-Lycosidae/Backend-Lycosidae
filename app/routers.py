# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlalchemy.orm import Session
from app.schemas import *
from app.utils import pass_hasher
from app.middleware import get_cookie_as_model, make_cookie_from_dict, make_cookie_from_model, get_current_user
from app.logger import get_logger

# Configuração do logger para este módulo
logger = get_logger(__name__)

router = APIRouter(
    tags=["backend"]
)

# Just for debugging before creating the interpreter
mock_users = []
mock_id_counter = 1

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,     # sempre em prod
    "samesite": "lax",  # mais seguro que none
    "max_age": 3600,    # 1h
}

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

# @router.get("/debug")
async def debug_state():
    """

    Debug endpoint (development only).

    Returns:
        - All mock users currently stored in memory.
        - Current value of the ID counter.

    """
    return {
        "mock_users": [
            {k: v for k, v in u.items()}
            for u in mock_users
        ],
        "id_counter": mock_id_counter
    }

@router.post("/register", response_model=UserReadDTO, status_code=201)
async def register(payload: UserCreateDTO):
    """

    Register a new user (mocked).

    Steps:
        1. Check if email is already registered.
        2. Hash the password and store in mock DB.
        3. Return UserReadDTO.

    """
    global mock_id_counter

    if any(u["email"] == payload.email for u in mock_users):
        raise HTTPException(400, detail="Email already registered")
    if any(u["username"] == payload.username for u in mock_users):
        raise HTTPException(400, detail="Username already taken")

    user = {
        "id": mock_id_counter,
        "username": payload.username,
        "email": payload.email,
        "password": pass_hasher(payload.password),
    }
    mock_users.append(user)
    mock_id_counter += 1

    response = JSONResponse(UserReadDTO(**user).model_dump())
    return response

@router.post("/login")
async def login(payload: UserLoginDTO):
    """
    Authenticate user (mocked).

    Steps:
        1. Find user by email.
        2. Compare hashed password.
        3. Return JWT in cookie if valid.
    """
    user = next((u for u in mock_users if u["email"] == payload.email), None)
    if not user or user["password"] != pass_hasher(payload.password):
        raise HTTPException(401, "Invalid credentials")

    token = make_cookie_from_model(
        AuthToken(id=user["id"], username=user["username"], email=user["email"], role="player")
    )

    response = JSONResponse({"message": "Login successful"})
    response.set_cookie("session_token", token, **COOKIE_SETTINGS)
    return response

@router.post("/logout")
async def logout():
    """
    Logout user by clearing the cookie.
    """
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("session_token")
    return response

@router.get("/me", response_model=UserReadDTO)
async def read_me(current_user: AuthToken = Depends(get_current_user)):
    """
    Get current logged-in user (mocked).
    """
    user = next((u for u in mock_users if u["id"] == current_user.id), None)
    if not user:
        raise HTTPException(404, "User not found")
    return UserReadDTO(id=user["id"], username=user["username"], email=user["email"])

@router.put("/me", response_model=UserReadDTO)
async def update_me(payload: UserUpdateDTO, current_user: AuthToken = Depends(get_current_user)):
    """
    Update current user info (mocked).
    """
    user = next((u for u in mock_users if u["id"] == current_user.id), None)
    if not user:
        raise HTTPException(404, "User not found")

    # Verify if already exists
    if payload.username:
        if any(u["username"] == payload.username and u["id"] != current_user.id for u in mock_users):
            raise HTTPException(400, detail="Username already taken")
        user["username"] = payload.username

    if payload.email:
        if any(u["email"] == payload.email and u["id"] != current_user.id for u in mock_users):
            raise HTTPException(400, detail="Email already registered")
        user["email"] = payload.email

    if payload.password:
        user["password"] = pass_hasher(payload.password)

    return UserReadDTO(id=user["id"], username=user["username"], email=user["email"])

@router.delete("/me")
async def delete_me(current_user: AuthToken = Depends(get_current_user)):
    """
    Delete current user account (mocked).
    """
    global mock_users
    before_count = len(mock_users)
    mock_users = [u for u in mock_users if u["id"] != current_user.id]

    if len(mock_users) == before_count:
        raise HTTPException(404, "User not found")

    response = JSONResponse({"message": "User deleted"})
    response.delete_cookie("session_token")
    return response