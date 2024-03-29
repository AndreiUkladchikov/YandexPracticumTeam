from config import settings
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    storage_uri=f"redis://{settings.redis_host}:{settings.redis_port}",
    default_limits=["5000 per day", "1000 per hour"],
    strategy="fixed-window",
    enabled=settings.rate_limit_enabled,
)
