from fastapi import APIRouter

router = APIRouter()

@router.post("/query")
async def query_document():
    # Build On Progress
    return {"message": "query endpoint coming soon"}