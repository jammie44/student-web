def process_ai_request(request_type: str, data: dict, user_id: int):
    if request_type == "cv":
        from backend.app.services.ai_service import generate_cv_content
        return generate_cv_content(data)
    elif request_type == "research":
        from backend.app.services.ai_service import summarize_research
        return summarize_research(data.get("text", ""))
    elif request_type == "assignment":
        from backend.app.services.ai_service import format_assignment
        return format_assignment(data.get("text", ""))
    elif request_type == "plagiarism":
        from backend.app.services.ai_service import detect_plagiarism
        return detect_plagiarism(data.get("text", ""))
    elif request_type == "rewrite":
        from backend.app.services.ai_service import rewrite_text
        return rewrite_text(data.get("text", ""))
    elif request_type == "study":
        from backend.app.services.ai_service import study_copilot
        return study_copilot(data.get("question", ""), data.get("context", ""))
    return "Unknown request type"