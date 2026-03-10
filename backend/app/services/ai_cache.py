import hashlib
from backend.app.core.config import settings

# Simple in-memory cache
cache = {}

def get_cache_key(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()


def get_cached_response(prompt: str) -> str:
    key = get_cache_key(prompt)
    return cache.get(key)


def set_cached_response(prompt: str, response: str, expire: int = 3600):
    key = get_cache_key(prompt)
    cache[key] = response