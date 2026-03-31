from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.database import Base, engine
from app.models.user import User          # noqa
from app.models.chat import Chat, Message # noqa
from app.models.daily_usage import DailyUsage  # noqa
from app.routes import auth, users, chat, admin, usage

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudyHub API",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = ["*"] if settings.frontend_url in ("*", "") else [o.strip() for o in settings.frontend_url.split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    errors = exc.errors()
    msg = errors[0].get("msg", "Validation error").replace("Value error, ", "") if errors else "Validation error"
    return JSONResponse(status_code=422, content={"detail": msg})


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(usage.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": settings.app_version}
