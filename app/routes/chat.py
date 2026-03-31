from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, field_validator
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.chat import Chat, Message
from app.models.daily_usage import DailyUsage
from app.utils.ai_service import get_ai_response, get_daily_limit

router = APIRouter(prefix="/api/chats", tags=["chats"])
VALID_TOOLS = ["study_assistant", "plagiarism", "cv_generator", "assignment", "research"]


class CreateChatRequest(BaseModel):
    tool: str
    title: Optional[str] = None

    @field_validator("tool")
    @classmethod
    def validate_tool(cls, v):
        if v not in VALID_TOOLS:
            raise ValueError(f"Invalid tool: {v}")
        return v


class SendMessageRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty.")
        if len(v) > 8000:
            raise ValueError("Message too long (max 8000 chars).")
        return v


def _check_daily_limit(user_id: str, plan: str, tool: str, db: Session):
    today = date.today()
    record = db.query(DailyUsage).filter(
        DailyUsage.user_id == user_id,
        DailyUsage.usage_date == today,
        DailyUsage.tool == tool,
    ).first()
    limit = get_daily_limit(plan, tool)
    used = record.count if record else 0
    if used >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit reached ({limit} messages/day on {plan} plan). Resets at midnight. Upgrade to Pro for more."
        )
    if record:
        record.count += 1
        record.updated_at = datetime.utcnow()
    else:
        db.add(DailyUsage(user_id=user_id, usage_date=today, tool=tool, count=1))
    db.commit()
    return used + 1, limit


@router.get("")
def list_chats(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.updated_at.desc()).all()
    result = []
    for c in chats:
        mc = db.query(func.count(Message.id)).filter(Message.chat_id == c.id).scalar()
        last = db.query(Message).filter(Message.chat_id == c.id).order_by(Message.created_at.desc()).first()
        result.append({"id": c.id, "user_id": c.user_id, "tool": c.tool, "title": c.title,
                        "created_at": c.created_at, "updated_at": c.updated_at,
                        "message_count": mc, "last_message": last.content[:80] if last else None})
    return {"chats": result}


@router.post("", status_code=201)
def create_chat(req: CreateChatRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    title = req.title or f"New {req.tool.replace('_', ' ').title()} chat"
    chat = Chat(user_id=current_user.id, tool=req.tool, title=title)
    db.add(chat); db.commit(); db.refresh(chat)
    return {"chat": {"id": chat.id, "user_id": chat.user_id, "tool": chat.tool, "title": chat.title,
                     "created_at": chat.created_at, "updated_at": chat.updated_at, "message_count": 0, "last_message": None}}


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    msgs = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
    return {"messages": [{"id": m.id, "chat_id": m.chat_id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in msgs]}


@router.post("/{chat_id}/messages")
def send_message(chat_id: str, req: SendMessageRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")

    used, limit = _check_daily_limit(current_user.id, current_user.plan, chat.tool, db)

    user_msg = Message(chat_id=chat.id, user_id=current_user.id, role="user", content=req.content)
    db.add(user_msg); db.flush()

    # History for multi-turn context
    prev = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
    history = [{"role": m.role, "content": m.content} for m in prev[:-1]]

    ai_content = get_ai_response(chat.tool, req.content, history)

    # Append daily limit warning if close to limit
    remaining = limit - used
    if remaining <= 3 and current_user.plan == "free":
        ai_content += f"\n\n---\n*⚡ {remaining} message{'s' if remaining != 1 else ''} left today on free plan. [Upgrade to Pro](/pricing) for 5× more daily messages.*"

    ai_msg = Message(chat_id=chat.id, user_id=current_user.id, role="assistant", content=ai_content)
    db.add(ai_msg)

    if chat.title.startswith("New ") and len(req.content) > 5:
        chat.title = req.content[:50] + ("…" if len(req.content) > 50 else "")
    chat.updated_at = datetime.utcnow()
    db.commit(); db.refresh(user_msg); db.refresh(ai_msg)

    return {
        "user_message": {"id": user_msg.id, "chat_id": user_msg.chat_id, "role": user_msg.role, "content": user_msg.content, "created_at": user_msg.created_at},
        "ai_message":   {"id": ai_msg.id,   "chat_id": ai_msg.chat_id,   "role": ai_msg.role,   "content": ai_msg.content,   "created_at": ai_msg.created_at},
    }


@router.delete("/{chat_id}")
def delete_chat(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    db.delete(chat); db.commit()
    return {"message": "Deleted."}
