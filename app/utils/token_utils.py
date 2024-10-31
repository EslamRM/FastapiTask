import aioredis
from app.core.config import settings

redis = aioredis.from_url(settings.REDIS_URL)

async def revoke_token(refresh_token: str):
    await redis.setex(refresh_token, settings.REFRESH_TOKEN_EXPIRE_DAYS, "revoked")
    return True

async def is_token_revoked(token: str) -> bool:
    return await redis.exists(token) == 1
