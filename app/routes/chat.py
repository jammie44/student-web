from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.chat import Chat, Message
from app.models.credits import UserCredits
from app.schemas.chat import CreateChatRequest, SendMessageRequest
from app.utils.ai_service import (
    answer_study_question, check_plagiarism,
    generate_cv, format_assignment, summarise_research,
    CREDIT_COSTS,
)

router = APIRouter(prefix="/api/chats", tags=["chats"])


def _get_or_create_credits(user_id: str, db: Session) -> UserCredits:
    record = db.query(UserCredits).filter(UserCredits.user_id == user_id).first()
    if not record:
        record = UserCredits(user_id=user_id, credits=100)
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


def _deduct_credits(user_id: str, tool: str, db: Session):
    cost = CREDIT_COSTS.get(tool, 2)
    record = _get_or_create_credits(user_id, db)
    if record.credits < cost:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient credits. This tool costs {cost} credits. You have {record.credits}."
        )
    record.credits -= cost
    db.commit()
    return cost


# ── GET /api/chats ────────────────────────────────────────────────────────────
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


# ── POST /api/chats ───────────────────────────────────────────────────────────
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


# ── GET /api/chats/{chat_id}/messages ─────────────────────────────────────────
@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
    return {
        "messages": [
            {"id": m.id, "chat_id": m.chat_id, "role": m.role, "content": m.content, "created_at": m.created_at}
            for m in messages
        ]
    }


# ── POST /api/chats/{chat_id}/messages ────────────────────────────────────────
@router.post("/{chat_id}/messages")
def send_message(
    chat_id: str,
    req: SendMessageRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")

    # Check and deduct credits
    _deduct_credits(current_user.id, chat.tool, db)

    # Save user message
    user_msg = Message(chat_id=chat.id, user_id=current_user.id, role="user", content=req.content)
    db.add(user_msg)
    db.flush()

    # Call the real AI based on tool
    try:
        if chat.tool == "study_assistant":
            # Pass conversation history for multi-turn context
            history = []
            prev_msgs = (
                db.query(Message)
                .filter(Message.chat_id == chat_id)
                .order_by(Message.created_at.asc())
                .all()
            )
            for m in prev_msgs[:-1]:  # exclude the just-added user message
                history.append({"role": m.role, "content": m.content})
            ai_content = answer_study_question(req.content, history)

        elif chat.tool == "plagiarism":
            ai_content = check_plagiarism(req.content)

        elif chat.tool == "cv_generator":
            ai_content = generate_cv(req.content)

        elif chat.tool == "assignment":
            ai_content = format_assignment(req.content)

        elif chat.tool == "research":
            ai_content = summarise_research(req.content)

        else:
            ai_content = answer_study_question(req.content)

    except RuntimeError as e:
        # API key not configured — return helpful error
        ai_content = (
            f"⚠️ AI service not configured: {str(e)}\n\n"
            "Please ask the administrator to set the ANTHROPIC_API_KEY "
            "environment variable in the Render dashboard."
        )
    except Exception as e:
        ai_content = f"⚠️ AI error: {str(e)}\n\nPlease try again in a moment."

    # Save AI message
    ai_msg = Message(chat_id=chat.id, user_id=current_user.id, role="assistant", content=ai_content)
    db.add(ai_msg)

    # Auto-title chat from first message
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


# ── DELETE /api/chats/{chat_id} ───────────────────────────────────────────────
@router.delete("/{chat_id}")
def delete_chat(chat_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted."}
