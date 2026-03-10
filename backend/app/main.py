from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints.auth import router as auth_router
from backend.app.api.v1.endpoints.cv import router as cv_router
from backend.app.api.v1.endpoints.assignments import router as assignments_router
from backend.app.api.v1.endpoints.research import router as research_router
from backend.app.api.v1.endpoints.plagiarism import router as plagiarism_router
from backend.app.api.v1.endpoints.ai_chat import router as ai_chat_router
from backend.app.api.v1.endpoints.billing import router as billing_router
from backend.app.api.v1.endpoints.admin import router as admin_router
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(cv_router, prefix="/api/v1/cv", tags=["cv"])
app.include_router(assignments_router, prefix="/api/v1/assignments", tags=["assignments"])
app.include_router(research_router, prefix="/api/v1/research", tags=["research"])
app.include_router(plagiarism_router, prefix="/api/v1/plagiarism", tags=["plagiarism"])
app.include_router(ai_chat_router, prefix="/api/v1/ai-chat", tags=["ai-chat"])
app.include_router(billing_router, prefix="/api/v1/billing", tags=["billing"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "Welcome to StudentHub API"}