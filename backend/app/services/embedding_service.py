from openai import OpenAI
from backend.app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=settings.embedding_model
    )
    return response.data[0].embedding