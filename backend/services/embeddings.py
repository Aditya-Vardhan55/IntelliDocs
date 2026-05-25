from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import get_settings
import structlog

logger = structlog.get_logger()
settings = get_settings()

# Load once at module import - not on every request
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        logger.info("loading_embedding_model", model=settings.embedding_model)
        _embedding_model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
            cache_folder=".model_cache"
        )
        logger.info("embedding_model_loaded")
    return _embedding_model
