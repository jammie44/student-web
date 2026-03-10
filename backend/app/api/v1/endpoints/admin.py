from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.models.subscription import Subscription
from backend.app.models.ai_requests import AIRequests
from backend.app.models.credits import UserCredits
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from sqlalchemy import func

router = APIRouter()

def admin_only(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/users")
def get_users(db: Session = Depends(get_db), admin: User = Depends(admin_only)):
    users = db.query(User).all()
    return users

@router.get("/subscriptions")
def get_subscriptions(db: Session = Depends(get_db), admin: User = Depends(admin_only)):
    subs = db.query(Subscription).all()
    return subs

@router.get("/ai-usage")
def get_ai_usage(db: Session = Depends(get_db), admin: User = Depends(admin_only)):
    usage = db.query(AIRequests).all()
    return usage

@router.get("/credit-consumption")
def get_credit_consumption(db: Session = Depends(get_db), admin: User = Depends(admin_only)):
    credits = db.query(UserCredits).all()
    return credits

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), admin: User = Depends(admin_only)):
    total_users = db.query(func.count(User.id)).scalar()
    total_subs = db.query(func.count(Subscription.id)).scalar()
    total_requests = db.query(func.count(AIRequests.id)).scalar()
    total_credits = db.query(func.sum(UserCredits.credits)).scalar()
    return {
        "total_users": total_users,
        "total_subscriptions": total_subs,
        "total_ai_requests": total_requests,
        "total_credits": total_credits
    }