from fastapi import APIRouter, UploadFile, File, HTTPException
import structlog

from backend.services.rag_pipeline import process_document

router = APIRouter()
logger = structlog.get_logger()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Only accept text and PDF for now
    allowed_types = ["text/plain", "application/pdf"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported. Use .txt or .pdf"
        )
        
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        logger.info("file_received", filename=file.filename, size=len(text))
        
        result = process_document(text=text, filename=file.filename)
        
        return {
            "status": "success",
            "message": f"Document processed successfully",
            "metadata": result
        }
    except Exception as e:
        logger.error("upload_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))