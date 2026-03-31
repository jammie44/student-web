from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.daily_usage import DailyUsage
from app.utils.ai_service import DAILY_LIMITS, get_daily_limit

router = APIRouter(prefix="/api/usage", tags=["usage"])
TOOLS = ["study_assistant", "plagiarism", "cv_generator", "assignment", "research"]


@router.get("/today")
def get_today_usage(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    records = db.query(DailyUsage).filter(DailyUsage.user_id == current_user.id, DailyUsage.usage_date == today).all()
    usage_map = {r.tool: r.count for r in records}
    plan = current_user.plan
    result = {}
    for tool in TOOLS:
        used = usage_map.get(tool, 0)
        limit = get_daily_limit(plan, tool)
        result[tool] = {"used": used, "limit": limit, "remaining": max(0, limit - used), "exhausted": used >= limit}
    return {"plan": plan, "date": str(today), "usage": result}
