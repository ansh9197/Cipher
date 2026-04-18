from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class FeedbackPayload(BaseModel):
    run_id:    str
    repo:      str
    rating:    int          # 1 = thumbs up, -1 = thumbs down
    category:  Optional[str] = None
    comment:   Optional[str] = None
    tenant_id: Optional[str] = None


@router.post("/feedback")
async def submit_feedback(payload: FeedbackPayload):
    """
    Receives feedback from engineers on analysis quality.
    Stores it for use in weekly retraining.
    """
    if payload.rating not in (1, -1):
        raise HTTPException(status_code=400, detail="rating must be 1 or -1")

    logger.info(
        f"Feedback received: run={payload.run_id} repo={payload.repo} "
        f"rating={'positive' if payload.rating == 1 else 'negative'} "
        f"category={payload.category}"
    )

    # TODO Phase 5: persist to PostgreSQL feedback table
    # For now we log it — the retraining job will query this table

    return {
        "status":  "recorded",
        "run_id":  payload.run_id,
        "message": "Thank you for your feedback. It will improve future analyses.",
    }
