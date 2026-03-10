from backend.app.services.embedding_service import get_embedding
from backend.app.vector_store.memory_vector_store import memory_store
from backend.app.models.user_memory import UserMemory
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal


def store_memory(user_id: int, memory_text: str):
    embedding = get_embedding(memory_text)
    memory_store.add_embedding(embedding, memory_text)
    db = SessionLocal()
    try:
        memory = UserMemory(user_id=user_id, memory_text=memory_text, embedding=embedding)
        db.add(memory)
        db.commit()
        memory_store.save()
    finally:
        db.close()


def retrieve_memories(user_id: int, query: str, k: int = 5) -> list[str]:
    embedding = get_embedding(query)
    return memory_store.search(embedding, k)


def get_user_memories_context(user_id: int, query: str) -> str:
    memories = retrieve_memories(user_id, query)
    return " ".join(memories)