import faiss
import numpy as np
import pickle
import os
from backend.app.core.config import settings


class FAISSStore:
    def __init__(self):
        self.dimension = 1536  # for text-embedding-3-small
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []

    def add_embedding(self, embedding: list[float], chunk: str):
        self.index.add(np.array([embedding], dtype=np.float32))
        self.chunks.append(chunk)

    def search(self, query_embedding: list[float], k: int = 5) -> list[str]:
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

    def save(self):
        faiss.write_index(self.index, settings.faiss_index_path)
        with open(settings.faiss_index_path + "_chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self):
        self.index = faiss.read_index(settings.faiss_index_path)
        with open(settings.faiss_index_path + "_chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)


faiss_store = FAISSStore()
if os.path.exists(settings.faiss_index_path):
    faiss_store.load()