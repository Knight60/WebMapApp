import time
from typing import Generic, TypeVar

T = TypeVar("T")


class TTLCache(Generic[T]):
    """Small in-memory TTL cache. Process-local; not shared across instances."""

    def __init__(self) -> None:
        self._store: dict[tuple, tuple[float, T]] = {}

    def get(self, key: tuple) -> T | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.monotonic() >= expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: tuple, value: T, ttl_seconds: float) -> None:
        self._store[key] = (time.monotonic() + ttl_seconds, value)
