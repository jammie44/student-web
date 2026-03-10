from backend.app.services.embedding_service import get_embedding
from backend.app.vector_store.faiss_store import faiss_store
from backend.app.services.ai_service import study_copilot


def retrieve_relevant_chunks(query: str, k: int = 5) -> list[str]:
    embedding = get_embedding(query)
    return faiss_store.search(embedding, k)


def generate_answer(query: str, context: str) -> str:
    return study_copilot(query, context)