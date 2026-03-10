from fastapi import APIRouter, Depends
from backend.app.services.ai_service import generate_cv_content
from backend.app.core.security import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.post("/generate")
def generate_cv(data: dict, current_user: User = Depends(get_current_user)):
    content = generate_cv_content(data)
    return {"content": content}