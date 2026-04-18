from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    email:     EmailStr
    password:  str
    full_name: Optional[str] = None
    company:   Optional[str] = None

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user_id:      str
    email:        str
    plan:         str

class UserResponse(BaseModel):
    id:                  UUID
    email:               str
    full_name:           Optional[str]
    company:             Optional[str]
    plan:                str
    is_active:           bool
    github_username:     Optional[str]
    analyses_this_month: int
    created_at:          datetime

    class Config:
        from_attributes = True
