from fastapi import APIRouter
from app.ml.model import get_model_version

router = APIRouter()

@router.get("/health")
async def health():
    mv = get_model_version()
    return {
        "status":        "ok",
        "service":       "inference-service",
        "model_version": mv if mv else "rule-based-fallback",
    }
