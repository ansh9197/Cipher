from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from app.ml.predictor import predict
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class PredictRequest(BaseModel):
    log_text: str
    metadata: Optional[Dict] = {}


class PredictResponse(BaseModel):
    category:   str
    confidence: float
    root_cause: str
    suggestion: str
    method:     str


@router.post("/predict", response_model=PredictResponse)
async def run_prediction(request: PredictRequest):
    if not request.log_text or len(request.log_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="log_text is too short")

    result = predict(
        log_text=request.log_text,
        metadata=request.metadata or {},
    )

    logger.info(f"Prediction: category={result['category']} confidence={result['confidence']} method={result['method']}")
    return PredictResponse(**result)
