from fastapi import APIRouter, Depends
from backend.app.services.ai_service import detect_plagiarism
from backend.app.core.security import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/detect")
def detect_plag(text: str, current_user: User = Depends(get_current_user)):
    content = detect_plagiarism(text)
    return {"content": content}