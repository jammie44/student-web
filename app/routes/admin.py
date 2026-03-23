from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.core.database import get_db
from app.core.security import require_admin
from app.models.user import User
from app.models.subscription import Subscription
from app.models.chat import Chat, Message

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    return {
        "total_users":    db.query(func.count(User.id)).scalar(),
        "active_users":   db.query(func.count(User.id)).filter(User.is_active == True).scalar(),
        "total_subs":     db.query(func.count(Subscription.id)).scalar(),
        "total_chats":    db.query(func.count(Chat.id)).scalar(),
        "total_messages": db.query(func.count(Message.id)).scalar(),
    }


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    query = db.query(User)
    if search:
        query = query.filter(User.email.ilike(f"%{search}%"))
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    result = []
    for user in users:
        chat_count = db.query(func.count(Chat.id)).filter(Chat.user_id == user.id).scalar()
        sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        result.append({
            "id": user.id, "email": user.email, "name": user.name,
            "is_active": user.is_active, "is_admin": user.is_admin,
            "created_at": user.created_at, "chat_count": chat_count,
            "plan": sub.plan if sub else "free",
        })
    return {"users": result, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.patch("/users/{user_id}/toggle")
def toggle_user(user_id: str, current_admin=Depends(require_admin), db: Session = Depends(get_db)):
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="You cannot disable your own account.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.is_active = not user.is_active
    db.commit()
    return {"user": {"id": user.id, "email": user.email, "is_active": user.is_active}}


@router.get("/subscriptions")
def list_subscriptions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    total = db.query(func.count(Subscription.id)).scalar()
    subs = db.query(Subscription).order_by(Subscription.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    result = []
    for sub in subs:
        user = db.query(User).filter(User.id == sub.user_id).first()
        result.append({
            "id": sub.id, "user_id": sub.user_id,
            "user_email": user.email if user else None,
            "user_name": user.name if user else None,
            "stripe_customer_id": sub.stripe_customer_id,
            "stripe_sub_id": sub.stripe_sub_id,
            "plan": sub.plan, "status": sub.status, "created_at": sub.created_at,
        })
    return {"subscriptions": result, "total": total, "page": page, "pages": max(1, -(-total // limit))}
