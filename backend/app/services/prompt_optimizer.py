from sqlalchemy.orm import Session
from backend.app.models.prompt_performance import PromptPerformance
from backend.app.core.database import SessionLocal


def log_performance(prompt_version: str, token_usage: int, response_time: float, user_rating: float = None, success_score: float = 0.0):
    db = SessionLocal()
    try:
        performance = PromptPerformance(
            prompt_version=prompt_version,
            token_usage=token_usage,
            response_time=response_time,
            user_rating=user_rating,
            success_score=success_score
        )
        db.add(performance)
        db.commit()
    finally:
        db.close()


def get_best_prompt_version() -> str:
    db = SessionLocal()
    try:
        # Get the prompt version with the highest average success_score
        result = db.query(PromptPerformance.prompt_version).group_by(PromptPerformance.prompt_version).order_by(
            db.func.avg(PromptPerformance.success_score).desc()
        ).first()
        return result[0] if result else "default"
    finally:
        db.close()


def optimize_prompt(base_prompt: str, context: dict) -> str:
    # Simple optimization: append context or select version
    version = get_best_prompt_version()
    if version == "v2":
        return f"Improved {base_prompt} with context: {context}"
    return base_prompt