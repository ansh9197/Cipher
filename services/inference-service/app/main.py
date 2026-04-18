from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import predict, health
from app.ml.model import load_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inference service starting — loading model...")
    load_model()
    logger.info("Model load attempt complete")
    yield
    logger.info("Inference service shutting down...")


app = FastAPI(
    title="CIPHER Inference Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,  tags=["health"])
app.include_router(predict.router, prefix="/api/v1", tags=["predict"])


@app.get("/")
async def root():
    return {"service": "cipher-inference", "status": "running"}
