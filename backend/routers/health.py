from fastapi import APIRouter
from backend.services.cache import get_cache_stats
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.get("/health")
async def health_check():
    logger.info("health_check_called")
    return {
        "status": "healthy",
        "service": "intellidocs-backend",
        "version": "0.1.0"
    }
    
@router.get("/health/detailed")
async def detailed_health():
    
    cache_stats = get_cache_stats()
    return {
        "status": "healthy",
        "components": {
            "api": "up",
            "chromadb": "up",
            "redis": cache_stats,
            "ollama": "up"
        }
    }