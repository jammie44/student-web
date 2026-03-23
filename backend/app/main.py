import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import Base, engine

# Import all models so SQLAlchemy registers them before create_all
from app.models import User, Subscription, Chat, Message  # noqa: F401

# Import routers
from app.routes import auth, users, chat, admin, billing

# ── Create tables on startup ──────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="StudyHub API",
    description="AI-powered academic platform backend",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
origins = (
    ["*"]
    if settings.frontend_url in ("*", "")
    else [o.strip() for o in settings.frontend_url.split(",")]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Validation error handler (returns clean JSON) ─────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    first = errors[0] if errors else {}
    msg = first.get("msg", "Validation error").replace("Value error, ", "")
    return JSONResponse(status_code=422, content={"detail": msg})

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(billing.router)

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "version": settings.app_version}

# ── Serve Next.js frontend static export (optional, for single-service deploys) ──
FRONTEND_OUT = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "out")
if os.path.isdir(FRONTEND_OUT):
    app.mount("/", StaticFiles(directory=FRONTEND_OUT, html=True), name="frontend")
