from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.schemas.auth import UserResponse
from typing import Optional
import uuid

router = APIRouter()

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_token(authorization.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    result = await db.execute(select(User).where(User.id == uuid.UUID(payload["sub"])))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me")
async def update_profile(
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    for key, value in updates.items():
        if key in ["full_name", "company"]:
            setattr(current_user, key, value)
    await db.flush()
    return {"status": "updated"}


from sqlalchemy import text

@router.get("/analyses")
async def get_analyses(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analyses for current user's tenant."""
    try:
        result = await db.execute(
            text("""
                SELECT id, run_id, repo, branch, workflow_name, conclusion,
                       category, confidence, root_cause, suggestion, method, created_at
                FROM analyses
                WHERE tenant_id = :tenant_id
                ORDER BY created_at DESC
                LIMIT 50
            """),
            {"tenant_id": str(current_user.id)}
        )
        rows = result.fetchall()
        return [dict(r._mapping) for r in rows]
    except Exception as e:
        return []


@router.get("/analyses")
async def get_user_analyses(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Return analyses for this user."""
    from sqlalchemy import text
    try:
        result = await db.execute(
            text("""
                SELECT id::text, run_id, repo, branch, workflow_name,
                       conclusion, category, confidence,
                       root_cause, suggestion, method,
                       created_at::text
                FROM analyses
                WHERE tenant_id = :tid
                ORDER BY created_at DESC LIMIT 50
            """),
            {"tid": str(current_user.id)}
        )
        rows = result.fetchall()
        return [dict(r._mapping) for r in rows]
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Analyses fetch error: {e}")
        return []
