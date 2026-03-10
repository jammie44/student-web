import faiss
import numpy as np
import pickle
import os
from backend.app.core.config import settings


class MemoryVectorStore:
    def __init__(self):
        self.dimension = 1536
        self.index = faiss.IndexFlatL2(self.dimension)
        self.memories = []

    def add_embedding(self, embedding: list[float], memory: str):
        self.index.add(np.array([embedding], dtype=np.float32))
        self.memories.append(memory)

    def search(self, query_embedding: list[float], k: int = 5) -> list[str]:
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        return [self.memories[i] for i in indices[0] if i < len(self.memories)]

    def save(self):
        path = settings.faiss_index_path + "_memory"
        faiss.write_index(self.index, path)
        with open(path + "_memories.pkl", "wb") as f:
            pickle.dump(self.memories, f)

    def load(self):
        path = settings.faiss_index_path + "_memory"
        if os.path.exists(path):
            self.index = faiss.read_index(path)
            with open(path + "_memories.pkl", "rb") as f:
                self.memories = pickle.load(f)


memory_store = MemoryVectorStore()
memory_store.load()