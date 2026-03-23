from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

VALID_TOOLS = ["study_assistant", "plagiarism", "cv_generator", "assignment", "research"]


class CreateChatRequest(BaseModel):
    tool: str
    title: Optional[str] = None

    @field_validator("tool")
    @classmethod
    def validate_tool(cls, v):
        if v not in VALID_TOOLS:
            raise ValueError(f"Tool must be one of: {', '.join(VALID_TOOLS)}")
        return v


class SendMessageRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty.")
        if len(v) > 5000:
            raise ValueError("Message too long (max 5000 characters).")
        return v


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: str
    user_id: str
    tool: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    last_message: Optional[str] = None

    class Config:
        from_attributes = True


class SendMessageResponse(BaseModel):
    user_message: MessageResponse
    ai_message: MessageResponse
