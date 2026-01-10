import time
from collections import defaultdict

REQUESTS = defaultdict(list)

def is_rate_limited(key, limit=5, window=60):
    """
    key    → identifier (IP / user / endpoint)
    limit  → max requests
    window → time window in seconds
    """
    now = time.time()

    REQUESTS[key] = [t for t in REQUESTS[key] if now - t < window]

    if len(REQUESTS[key]) >= limit:
        return True

    REQUESTS[key].append(now)
    return False
