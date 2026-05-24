from fastapi import APIRouter
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
    # Will expand this to check ChromaDB, Redis, Ollama later
    return {
        "status": "healthy",
        "components": {
            "api": "up",
            "chromadb": "not_checked_yet",
            "redis": "not_checked_yet",
            "ollama": "not_checked_yet"
        }
    }