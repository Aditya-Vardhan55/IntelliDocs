from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_document():
    # Build In Progress
    return {"message": "upload endpoint coming soon"}