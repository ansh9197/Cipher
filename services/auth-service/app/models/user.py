from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid, enum
from app.core.database import Base

class PlanType(str, enum.Enum):
    free       = "free"
    starter    = "starter"
    pro        = "pro"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"

    id                     = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email                  = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password        = Column(String(255), nullable=False)
    full_name              = Column(String(255), nullable=True)
    company                = Column(String(255), nullable=True)
    is_active              = Column(Boolean, default=True)
    is_verified            = Column(Boolean, default=False)
    plan                   = Column(SAEnum(PlanType), default=PlanType.free, nullable=False)
    stripe_customer_id     = Column(String(255), nullable=True, unique=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    github_installation_id = Column(String(255), nullable=True)
    github_username        = Column(String(255), nullable=True)
    analyses_this_month    = Column(Integer, default=0)
    created_at             = Column(DateTime(timezone=True), server_default=func.now())
    updated_at             = Column(DateTime(timezone=True), onupdate=func.now())
