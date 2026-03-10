from openai import OpenAI
from backend.app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_cv_content(user_data: dict) -> str:
    prompt = f"Generate a professional CV based on the following information: {user_data}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content


def summarize_research(text: str) -> str:
    prompt = f"Summarize the following research text: {text}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content


def format_assignment(text: str) -> str:
    prompt = f"Format the following assignment text professionally: {text}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content


def detect_plagiarism(text: str) -> str:
    prompt = f"Analyze the following text for plagiarism and provide a report: {text}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content


def rewrite_text(text: str) -> str:
    prompt = f"Rewrite the following text to improve clarity and grammar: {text}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content


def study_copilot(question: str, context: str = "") -> str:
    prompt = f"Answer the student's question: {question}. Context: {context}"
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.max_tokens
    )
    return response.choices[0].message.content