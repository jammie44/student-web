from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.chat import Chat, Message
from app.schemas.chat import CreateChatRequest, SendMessageRequest
from app.utils.ai_responses import get_ai_response

router = APIRouter(prefix="/api/chats", tags=["chats"])


@router.get("")
def list_chats(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == current_user.id)
        .order_by(Chat.updated_at.desc())
        .all()
    )
    result = []
    for chat in chats:
        msg_count = db.query(func.count(Message.id)).filter(Message.chat_id == chat.id).scalar()
        last = db.query(Message).filter(Message.chat_id == chat.id).order_by(Message.created_at.desc()).first()
        result.append({
            "id": chat.id, "user_id": chat.user_id, "tool": chat.tool, "title": chat.title,
            "created_at": chat.created_at, "updated_at": chat.updated_at,
            "message_count": msg_count,
            "last_message": last.content[:80] if last else None,
        })
    return {"chats": result}


@router.post("", status_code=201)
def create_chat(req: CreateChatRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    title = req.title or f"New {req.tool.replace('_', ' ').title()} chat"
    chat = Chat(user_id=current_user.id, tool=req.tool, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {"chat": {
        "id": chat.id, "user_id": chat.user_id, "tool": chat.tool, "title": chat.title,
        "created_at": chat.created_at, "updated_at": chat.updated_at,
        "message_count": 0, "last_message": None,
    }}


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
    return {"messages": [{"id": m.id, "chat_id": m.chat_id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]}


@router.post("/{chat_id}/messages")
def send_message(chat_id: str, req: SendMessageRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")

    user_msg = Message(chat_id=chat.id, user_id=current_user.id, role="user", content=req.content)
    db.add(user_msg)
    db.flush()

    ai_content = get_ai_response(chat.tool)
    ai_msg = Message(chat_id=chat.id, user_id=current_user.id, role="assistant", content=ai_content)
    db.add(ai_msg)

    if chat.title.startswith("New ") and len(req.content) > 5:
        chat.title = req.content[:50] + ("…" if len(req.content) > 50 else "")
    chat.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user_msg)
    db.refresh(ai_msg)

    return {
        "user_message": {"id": user_msg.id, "chat_id": user_msg.chat_id, "role": user_msg.role, "content": user_msg.content, "created_at": user_msg.created_at},
        "ai_message":   {"id": ai_msg.id,   "chat_id": ai_msg.chat_id,   "role": ai_msg.role,   "content": ai_msg.content,   "created_at": ai_msg.created_at},
    }


@router.delete("/{chat_id}")
def delete_chat(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted."}
