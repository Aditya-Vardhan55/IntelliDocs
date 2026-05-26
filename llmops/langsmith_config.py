import os
import structlog
from backend.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

def setup_langsmith():
    """
    Configures LangSmith tracing by setting environment variables.
    LangChain automatically picks these up and sends traces to LangSmith.
    No manual intrumentation needed - it hooks into LangChain automatically.
    """
    if not settings.langchain_api_key:
        logger.warning("langsmith_disabled", reason="no API key provided")
        return False
    
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    
    logger.info("langsmith_enabled", project=settings.langchain_project)
    return True