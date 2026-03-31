from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.core.database import get_db
from app.core.security import require_admin
from app.models.user import User
from app.models.chat import Chat, Message

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    return {
        "total_users":    db.query(func.count(User.id)).scalar(),
        "active_users":   db.query(func.count(User.id)).filter(User.is_active == True).scalar(),
        "pro_users":      db.query(func.count(User.id)).filter(User.plan == "pro").scalar(),
        "total_chats":    db.query(func.count(Chat.id)).scalar(),
        "total_messages": db.query(func.count(Message.id)).scalar(),
    }


@router.get("/users")
def list_users(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
               search: Optional[str] = Query(None), db: Session = Depends(get_db), _=Depends(require_admin)):
    q = db.query(User)
    if search:
        q = q.filter(User.email.ilike(f"%{search}%"))
    total = q.count()
    users = q.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    result = []
    for u in users:
        cc = db.query(func.count(Chat.id)).filter(Chat.user_id == u.id).scalar()
        result.append({"id": u.id, "email": u.email, "name": u.name, "is_active": u.is_active,
                        "is_admin": u.is_admin, "plan": u.plan, "created_at": u.created_at, "chat_count": cc})
    return {"users": result, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.patch("/users/{user_id}/toggle")
def toggle_user(user_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot disable your own account.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.is_active = not user.is_active
    db.commit()
    return {"user": {"id": user.id, "email": user.email, "is_active": user.is_active}}


@router.patch("/users/{user_id}/plan")
def change_plan(user_id: str, req: dict, admin=Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    plan = req.get("plan", "free")
    if plan not in ["free", "pro", "unlimited"]:
        raise HTTPException(status_code=400, detail="Invalid plan.")
    user.plan = plan
    db.commit()
    return {"user": {"id": user.id, "email": user.email, "plan": user.plan}}
