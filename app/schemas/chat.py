from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
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
    model_config = ConfigDict(from_attributes=True)

    id: str
    chat_id: str
    role: str
    content: str
    created_at: datetime
