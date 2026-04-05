from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.post("/quote")
async def submit_quote(payload: QuoteSubmission) -> dict: