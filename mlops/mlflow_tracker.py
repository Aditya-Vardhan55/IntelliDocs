import mlflow
import time
import structlog
from backend.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

def setup_mlflow():
    """
    Points MLflow at our local tracking server.
    All experiments get logged here and visible in MLflow UI.
    """
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("intellidocs-rag")
    logger.info("mlflow_configured", uri=settings.mlflow_tracking_uri)

def log_document_processing(
    filename: str,
    domain: str,
    chunk_size: int,
    chunk_overlap: int,
    num_chunks: int,
    processing_time: float
):
    """
    Logs a document processing run to MLflow.
    Each upload becomes one MLflow 'run' with:
    - Parameters: the settings we used (chunk size, overlap)
    - Metrics: the results (how many chunks, how fast)
    - Tags: metadata (filename, domain)
    This is how we compare strategies later.
    """
    with mlflow.start_run():
        # Parameters — what settings did we use?
        mlflow.log_param("domain", domain)
        mlflow.log_param("chunk_size", chunk_size)
        mlflow.log_param("chunk_overlap", chunk_overlap)
        mlflow.log_param("filename", filename)

        # Metrics — what were the results?
        mlflow.log_metric("num_chunks", num_chunks)
        mlflow.log_metric("processing_time_seconds", processing_time)
        mlflow.log_metric("chunks_per_second",
                          num_chunks / processing_time if processing_time > 0 else 0)

        # Tags — searchable metadata
        mlflow.set_tag("domain", domain)
        mlflow.set_tag("filename", filename)

        logger.info("mlflow_run_logged",
                    domain=domain,
                    num_chunks=num_chunks,
                    processing_time=processing_time)

def log_query(
    question: str,
    domain: str,
    response_time: float,
    num_source_chunks: int
):
    """
    Logs every query to MLflow.
    Tracks how fast queries are and how many chunks
    were retrieved — useful for tuning retrieval quality.
    """
    with mlflow.start_run():
        mlflow.log_param("domain", domain)
        mlflow.log_param("question_length", len(question))

        mlflow.log_metric("response_time_seconds", response_time)
        mlflow.log_metric("source_chunks_retrieved", num_source_chunks)

        mlflow.set_tag("query_domain", domain)

        logger.info("mlflow_query_logged",
                    domain=domain,
                    response_time=response_time)