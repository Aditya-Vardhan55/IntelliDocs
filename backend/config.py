from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    
    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "intellidocs"
    
    # AWS
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = "intellidocs-docs"
    
    # App
    app_env: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()