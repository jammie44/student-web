from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, hash_password, verify_password
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_profile(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name,
            "is_active": current_user.is_active, "is_admin": current_user.is_admin,
            "plan": current_user.plan, "created_at": current_user.created_at}


@router.patch("/me")
def update_profile(req: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if "name" in req:
        user.name = req["name"].strip()
    if "new_password" in req and req["new_password"]:
        if not verify_password(req.get("current_password", ""), user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")
        user.password = hash_password(req["new_password"])
    db.commit()
    return {"id": user.id, "email": user.email, "name": user.name, "plan": user.plan}
