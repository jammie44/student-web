from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    chat_count: int = 0
    plan: str = "free"
