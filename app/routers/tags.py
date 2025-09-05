"""
Rotas relacionadas às tags
"""
from fastapi import APIRouter, Request

try:
    from ..schemas import TagCreateDTO, TagReadDTO
    from ..logger import get_logger
    from ..rate_limiter import rate_limit_middleware
    from ..exceptions import ValidationException
    from ..security import SecurityUtils
except ImportError:
    from schemas import TagCreateDTO, TagReadDTO
    from logger import get_logger
    from rate_limiter import rate_limit_middleware
    from exceptions import ValidationException
    from security import SecurityUtils

logger = get_logger(__name__)
router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/",
            description="Create Tag Endpoint",
            summary="Create Tag Endpoint",
            response_model=TagReadDTO,
            status_code=201)
@rate_limit_middleware("create_tag", 10)
def create_tag_endpoint(tag_data: TagCreateDTO, request: Request):
    logger.info(f"Creating tag: {tag_data.type}")
    
    tag_data.type = SecurityUtils.sanitize_input(tag_data.type)
    
    logger.info(f"Tag created successfully: {tag_data.type}")
    
    return TagReadDTO(
        id="1",
        type=tag_data.type
    )

@router.get("/{tag_id}",
           description="Get Tag Endpoint",
           summary="Get Tag Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("get_tag", 60)
def get_tag_endpoint(tag_id: str, request: Request):
    logger.info(f"Getting tag: {tag_id}")
    
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    logger.info(f"Tag retrieved: {tag_id}")
    
    return TagReadDTO(
        id=tag_id,
        type="Sample Tag"
    )

@router.put("/{tag_id}",
           description="Update Tag Endpoint",
           summary="Update Tag Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("update_tag", 20)
def update_tag_endpoint(tag_id: str, tag_data: TagCreateDTO, request: Request):
    logger.info(f"Updating tag: {tag_id}")
    
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    tag_data.type = SecurityUtils.sanitize_input(tag_data.type)
    
    logger.info(f"Tag updated successfully: {tag_id}")
    
    return TagReadDTO(
        id=tag_id,
        type=tag_data.type
    )

@router.delete("/{tag_id}",
             description="Delete Tag Endpoint",
             summary="Delete Tag Endpoint",
             response_model=dict)
@rate_limit_middleware("delete_tag", 10)
def delete_tag_endpoint(tag_id: str, request: Request):
    logger.info(f"Deleting tag: {tag_id}")
    
    if not tag_id or len(tag_id) < 1:
        raise ValidationException("Invalid tag ID")
    
    logger.info(f"Tag deleted successfully: {tag_id}")
    
    return {"message": "Tag deleted successfully"}

@router.get("/type/{tag_type}",
           description="Get Tag By Type Endpoint",
           summary="Get Tag By Type Endpoint",
           response_model=TagReadDTO)
@rate_limit_middleware("get_tag_by_type", 60)
def get_tag_by_type_endpoint(tag_type: str, request: Request):
    logger.info(f"Getting tag by type: {tag_type}")
    
    if not tag_type or len(tag_type) < 1:
        raise ValidationException("Invalid tag type")
    
    tag_type = SecurityUtils.sanitize_input(tag_type)
    
    logger.info(f"Tag retrieved by type: {tag_type}")
    
    return TagReadDTO(
        id="1",
        type=tag_type
    )
