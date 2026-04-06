from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["quote"])

@router.get("/quote")
async def submit_quote(payload: QuoteSubmission) -> dict: