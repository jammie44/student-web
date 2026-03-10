from fastapi import APIRouter, Depends
from backend.app.services.ai_service import format_assignment
from backend.app.core.security import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/format")
def format_assign(text: str, current_user: User = Depends(get_current_user)):
    content = format_assignment(text)
    return {"content": content}