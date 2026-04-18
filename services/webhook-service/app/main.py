from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import webhook, health
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CIPHER Webhook Service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,  tags=["health"])
app.include_router(webhook.router, prefix="/api/v1/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {"service": "cipher-webhook", "status": "running"}
