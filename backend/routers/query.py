from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import structlog

from backend.services.rag_pipeline import query_document

router = APIRouter()
logger = structlog.get_logger()

class QueryRequest(BaseModel):
    question: str
    domain: str     # legal, medical, corporate, code

@router.post("/query")
async def query_document(request: QueryRequest):
    valid_domains = ["legal", "medical", "corporate", "code"]
    
    if request.domain not in valid_domains:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid domain. Choose from: {valid_domains}"
        )
        
    try:
        result = query_document(
            question=request.question,
            domain_str=request.domain
        )
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        logger.error("query_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))