from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=Token, status_code=201)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        company=payload.company,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = create_access_token({
        "sub":       str(user.id),
        "email":     user.email,
        "plan":      user.plan.value,
        "tenant_id": str(user.id)
    })
    logger.info(f"Registered: {user.email}")
    return Token(access_token=token, user_id=str(user.id), email=user.email, plan=user.plan.value)

@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    token = create_access_token({
        "sub":       str(user.id),
        "email":     user.email,
        "plan":      user.plan.value,
        "tenant_id": str(user.id)
    })
    return Token(access_token=token, user_id=str(user.id), email=user.email, plan=user.plan.value)
