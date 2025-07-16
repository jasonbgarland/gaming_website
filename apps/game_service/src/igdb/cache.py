"""
In-memory cache implementation for IGDB client.
Provides basic get/set/delete/clear operations with TTL support.
Not suitable for production use—see README for Redis recommendation.
"""

from typing import Any, Optional
import time
import threading


class InMemoryCache:
    """
    Simple in-memory cache with TTL support. Not thread-safe for production, but fine for local/dev.
    """

    def __init__(self):
        self._store = {}
        self._lock = threading.Lock()

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """Set a value in the cache with a time-to-live (in seconds)."""
        expire_at = time.time() + ttl if ttl else None
        with self._lock:
            self._store[key] = (value, expire_at)

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache, or None if not found or expired."""
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            value, expire_at = item
            if expire_at and expire_at < time.time():
                del self._store[key]
                return None
            return value

    def delete(self, key: str) -> None:
        """Delete a key from the cache."""
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        """Clear the entire cache."""
        with self._lock:
            self._store.clear()
