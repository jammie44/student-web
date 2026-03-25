from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.credits import UserCredits

router = APIRouter(prefix="/api/credits", tags=["credits"])


def _get_or_create(user_id: str, db: Session) -> UserCredits:
    record = db.query(UserCredits).filter(UserCredits.user_id == user_id).first()
    if not record:
        record = UserCredits(user_id=user_id, credits=100)
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


@router.get("/balance")
def get_balance(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    record = _get_or_create(current_user.id, db)
    return {
        "credits": record.credits,
        "user_id": current_user.id,
        "costs": {
            "study_assistant": 2,
            "plagiarism": 3,
            "cv_generator": 5,
            "assignment": 4,
            "research": 3,
        }
    }
