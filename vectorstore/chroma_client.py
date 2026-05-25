import chromadb
from chromadb.config import Settings
from backend.config import get_settings

settings = get_settings()

def get_chroma_client():
    client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb",
            anonymized_telemetry=False
        )
    )
    return client

def get_or_create_collection(client, collectio_name: str):
    collection = client.get_or_create_collection(
        name=collectio_name,
        metadata={"hnsw:space": "cosine"}
    )
    return collection