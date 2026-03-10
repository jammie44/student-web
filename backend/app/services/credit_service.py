from backend.app.models.credits import UserCredits
from sqlalchemy.orm import Session


def get_user_credits(user_id: int, db: Session) -> int:
    credits = db.query(UserCredits).filter(UserCredits.user_id == user_id).first()
    return credits.credits if credits else 0


def deduct_credits(user_id: int, amount: int, db: Session) -> bool:
    credits = db.query(UserCredits).filter(UserCredits.user_id == user_id).first()
    if credits and credits.credits >= amount:
        credits.credits -= amount
        db.commit()
        return True
    return False


def add_credits(user_id: int, amount: int, db: Session):
    credits = db.query(UserCredits).filter(UserCredits.user_id == user_id).first()
    if credits:
        credits.credits += amount
    else:
        credits = UserCredits(user_id=user_id, credits=amount)
        db.add(credits)
    db.commit()