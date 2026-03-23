import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import Base, engine

# Register all models with SQLAlchemy before create_all
from app.models import User, Subscription, Chat, Message  # noqa: F401

# Import routers
from app.routes import auth, users, chat, admin, billing

# Create all tables on startup (safe — skips existing tables)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudyHub API",
    description="AI-powered academic platform",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS — lock to FRONTEND_URL in production
origins = ["*"] if settings.frontend_url in ("*", "") else [o.strip() for o in settings.frontend_url.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Clean validation error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    first = errors[0] if errors else {}
    msg = first.get("msg", "Validation error").replace("Value error, ", "")
    return JSONResponse(status_code=422, content={"detail": msg})


# Register all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(billing.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": settings.app_version}
