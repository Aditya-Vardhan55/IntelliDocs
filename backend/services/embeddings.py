from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import get_settings
import structlog

logger = structlog.get_logger()
settings = get_settings()

def get_embedding_model():
    logger.info("loading_embedding_model", model=settings.embedding_model)
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    logger.info("embedding_model_loaded")
    return embeddings
