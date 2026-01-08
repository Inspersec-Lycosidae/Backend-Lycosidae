from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importação dos módulos de router
from app.routers import (auth, competitions, exercises, containers, tags, attendance, scoreboard)
from app.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Lycosidae Backend API",
    description="API Gateway responsável pela orquestração e validação de regras de negócio do sistema Lycosidae CTF.",
    version="1.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registo de todos os Routers no sistema
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(competitions.router, prefix="/competitions", tags=["competitions"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(containers.router, prefix="/containers", tags=["containers"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(scoreboard.router, prefix="/scoreboard", tags=["scoreboard"])

@app.get("/", tags=["system"])
def read_root():
    return {"message": "Bem-vindo ao Lycosidae Gateway API"}

@app.get("/healthy", description="Endpoint para verificação de saúde do sistema", tags=["system"])
def health_check():
    return {
        "status": "healthy",
        "service": "Backend-Lycosidae (Gateway)",
        "version": "1.1.0"
    }