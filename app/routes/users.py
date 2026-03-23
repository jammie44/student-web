from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user, hash_password, verify_password
from app.models.user import User
from app.models.subscription import Subscription
from app.models.chat import Chat, Message
from app.schemas.auth import UserResponse, UpdateProfileRequest

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_profile(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat_count = db.query(func.count(Chat.id)).filter(Chat.user_id == current_user.id).scalar()
    msg_count = db.query(func.count(Message.id)).filter(Message.user_id == current_user.id).scalar()
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at,
        "chat_count": chat_count,
        "message_count": msg_count,
        "subscription": {
            "plan": sub.plan if sub else "free",
            "status": sub.status if sub else "none",
        },
    }


@router.patch("/me", response_model=UserResponse)
def update_profile(req: UpdateProfileRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    update_data = {}
    if req.name is not None:
        update_data["name"] = req.name.strip()
    if req.new_password:
        if not req.current_password:
            raise HTTPException(status_code=400, detail="Current password is required.")
        if not verify_password(req.current_password, user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")
        if len(req.new_password) < 8:
            raise HTTPException(status_code=400, detail="New password must be at least 8 characters.")
        update_data["password"] = hash_password(req.new_password)
    if update_data:
        db.query(User).filter(User.id == current_user.id).update(update_data)
        db.commit()
        db.refresh(user)
    return user
