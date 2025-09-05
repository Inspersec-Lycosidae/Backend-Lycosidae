"""
Módulo de routers da API
"""
from fastapi import APIRouter

from .users import router as users_router
from .competitions import router as competitions_router
from .exercises import router as exercises_router
from .tags import router as tags_router
from .teams import router as teams_router
from .containers import router as containers_router
from .relationships import router as relationships_router
from .system import router as system_router

# Router principal que agrega todos os sub-routers
main_router = APIRouter(prefix="/route", tags=["main"])

# Incluir todos os routers
main_router.include_router(users_router)
main_router.include_router(competitions_router)
main_router.include_router(exercises_router)
main_router.include_router(tags_router)
main_router.include_router(teams_router)
main_router.include_router(containers_router)
main_router.include_router(relationships_router)

# Router do sistema (sem prefixo /route)
system_router_main = APIRouter()
system_router_main.include_router(system_router)

