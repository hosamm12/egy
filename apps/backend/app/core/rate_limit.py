import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from app.core.config import settings

_hits: dict[str, deque] = defaultdict(deque)


def limit_login(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = settings.RATE_LIMIT_WINDOW_SECONDS
    bucket = _hits[f"login:{ip}"]
    while bucket and now - bucket[0] > window:
        bucket.popleft()
    if len(bucket) >= settings.RATE_LIMIT_LOGIN:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts")
    bucket.append(now)
