from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.routes import auth, users, billing, health
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Auth service starting...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready")
    yield
    logger.info("Auth service shutting down...")

app = FastAPI(
    title="CIPHER Auth Service",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://cipher.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router,    prefix="/api/v1/auth",    tags=["auth"])
app.include_router(users.router,   prefix="/api/v1/users",   tags=["users"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])

@app.get("/")
async def root():
    return {"service": "cipher-auth", "status": "running"}
