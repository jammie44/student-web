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


class AdminSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    user_email: Optional[str]
    user_name: Optional[str]
    stripe_customer_id: Optional[str]
    stripe_sub_id: Optional[str]
    plan: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_subs: int
    total_chats: int
    total_messages: int


class PaginatedUsers(BaseModel):
    users: List[AdminUserResponse]
    total: int
    page: int
    pages: int


class PaginatedSubs(BaseModel):
    subscriptions: List[AdminSubscriptionResponse]
    total: int
    page: int
    pages: int
