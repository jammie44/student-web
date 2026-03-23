import re
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_access_token, get_current_user
)
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse, UpdateProfileRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])

# ── POST /api/auth/register ──────────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Block duplicate emails
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists. Please sign in instead.",
        )

    user = User(
        email=req.email,
        password=hash_password(req.password),
        name=req.name,
    )
    db.add(user)
    db.flush()

    # Free subscription on signup
    db.add(Subscription(user_id=user.id, plan="free", status="active"))
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


# ── POST /api/auth/login ─────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()

    # No account found
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account found with this email. Please create one first.",
        )

    # Account locked?
    if user.locked_until and datetime.utcnow() < user.locked_until:
        remaining = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
        raise HTTPException(
            status_code=423,
            detail=f"Account temporarily locked due to too many failed attempts. Try again in {remaining} minute(s).",
        )

    # Disabled?
    if not user.is_active:
        raise HTTPException(status_code=403, detail="This account has been disabled.")

    # Wrong password
    if not verify_password(req.password, user.password):
        new_failed = user.failed_logins + 1
        update_data = {"failed_logins": new_failed}

        if new_failed >= 5:
            update_data["locked_until"] = datetime.utcnow() + timedelta(minutes=15)
            update_data["failed_logins"] = 0

        db.query(User).filter(User.id == user.id).update(update_data)
        db.commit()

        attempts_left = max(0, 5 - new_failed)
        suggest_reset = new_failed >= 2

        raise HTTPException(
            status_code=401,
            detail="Incorrect password.",
            headers={
                "X-Suggest-Reset": "true" if suggest_reset else "false",
                "X-Attempts-Left": str(attempts_left),
            },
        )

    # Success — reset failed login counter
    db.query(User).filter(User.id == user.id).update(
        {"failed_logins": 0, "locked_until": None}
    )
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


# ── GET /api/auth/me ─────────────────────────────────────────────────────────
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ── POST /api/auth/logout ─────────────────────────────────────────────────────
@router.post("/logout")
def logout():
    # JWT is stateless; client clears the token
    return {"message": "Logged out successfully"}
