"""
Rotas relacionadas aos containers
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import ContainerCreateDTO, ContainerReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException
    from ..security import SecurityUtils
except ImportError:
    from schemas import ContainerCreateDTO, ContainerReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException
    from security import SecurityUtils

logger = get_logger(__name__)
router = APIRouter(prefix="/containers", tags=["containers"])

@router.post("/",
            description="Create Container Endpoint",
            summary="Create Container Endpoint",
            status_code=201)
@rate_limit_middleware("create_container", 10)
def create_container_endpoint(container_data: ContainerCreateDTO, request: Request):
    logger.info(f"Creating container with deadline: {container_data.deadline}")
    
    container_data.deadline = SecurityUtils.sanitize_input(container_data.deadline)
    
    logger.info(f"Container created successfully")
    
    return {"message": "Container created successfully"}

@router.get("/{container_id}",
           description="Get Container Endpoint",
           summary="Get Container Endpoint",
           response_model=ContainerReadDTO)
@rate_limit_middleware("get_container", 60)
def get_container_endpoint(container_id: str, request: Request):
    logger.info(f"Getting container: {container_id}")
    
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    logger.info(f"Container retrieved: {container_id}")
    
    return ContainerReadDTO(
        id=container_id,
        deadline="2024-12-31T23:59:59Z"
    )

@router.put("/{container_id}",
           description="Update Container Endpoint",
           summary="Update Container Endpoint",
           response_model=ContainerReadDTO)
@rate_limit_middleware("update_container", 20)
def update_container_endpoint(container_id: str, container_data: ContainerCreateDTO, request: Request):
    logger.info(f"Updating container: {container_id}")
    
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    container_data.deadline = SecurityUtils.sanitize_input(container_data.deadline)
    
    logger.info(f"Container updated successfully: {container_id}")
    
    return ContainerReadDTO(
        id=container_id,
        deadline=container_data.deadline
    )

@router.delete("/{container_id}",
             description="Delete Container Endpoint",
             summary="Delete Container Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_container", 10)
def delete_container_endpoint(container_id: str, request: Request):
    logger.info(f"Deleting container: {container_id}")
    
    if not container_id or len(container_id) < 1:
        raise ValidationException("Invalid container ID")
    
    logger.info(f"Container deleted successfully: {container_id}")
    
    return {"message": "Container deleted successfully"}
