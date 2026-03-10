from fastapi import APIRouter, Depends
from backend.app.services.ai_service import study_copilot
from backend.app.core.security import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/ask")
def ask_question(question: str, current_user: User = Depends(get_current_user)):
    answer = study_copilot(question)
    return {"answer": answer}