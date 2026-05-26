from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import structlog

from backend.routers import health, upload, query
from backend.config import get_settings
from llmops.langsmith_config import setup_langsmith
from mlops.mlflow_tracker import setup_mlflow

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

settings = get_settings()
logger = structlog.get_logger()

app = FastAPI(
    title="IntelliDocs",
    description="Universal Document Intelligence Platform",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics - auto instruments all endpoints
Instrumentator().instrument(app).expose(app)

# Routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(query.router, prefix="/api/v1", tags=["Query"])

@app.on_event("startup")
async def startup_event():
    logger.info("intellidocs_starting", env=settings.app_env)
    
    # Initialize Langsmith tracing
    langsmith_enabled = setup_langsmith()
    logger.info("langsmith_status", enabled=langsmith_enabled)
    
    # Initialize MLflow tracking
    setup_mlflow()
    logger.info("mlflow_status", uri=settings.mlflow_tracking_uri)
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("intellidocs_stopping")