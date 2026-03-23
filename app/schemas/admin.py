from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AdminUserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    chat_count: int = 0
    plan: str = "free"

    class Config:
        from_attributes = True
