from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain at least one number.")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    name: Optional[str] = None
    is_active: bool
    is_admin: bool
    plan: str
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/register", response_model=TokenOut, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Strict unique email — one Gmail = one account forever
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists. Please sign in instead.")
    user = User(email=req.email, password=hash_password(req.password), name=req.name, plan="free")
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.id})
    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenOut)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email. Please register first.")
    if user.locked_until and datetime.utcnow() < user.locked_until:
        mins = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
        raise HTTPException(status_code=423, detail=f"Account locked. Try again in {mins} minute(s).")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled. Contact support.")
    if not verify_password(req.password, user.password):
        new_fail = user.failed_logins + 1
        upd = {"failed_logins": new_fail}
        if new_fail >= 5:
            upd["locked_until"] = datetime.utcnow() + timedelta(minutes=15)
            upd["failed_logins"] = 0
        db.query(User).filter(User.id == user.id).update(upd)
        db.commit()
        raise HTTPException(status_code=401, detail="Incorrect password.")
    db.query(User).filter(User.id == user.id).update({"failed_logins": 0, "locked_until": None})
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.id})
    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout():
    return {"message": "Logged out"}
