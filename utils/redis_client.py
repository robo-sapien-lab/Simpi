"""
Redis client utilities and connection management.
"""
from typing import Optional
import aioredis
import structlog

logger = structlog.get_logger()

async def init_redis_pool(redis_url: str) -> aioredis.Redis:
    """Initialize Redis connection pool."""
    try:
        redis = await aioredis.from_url(
            redis_url,
            encoding='utf-8',
            decode_responses=True
        )
        
        # Test connection
        await redis.ping()
        logger.info("Redis connection established")
        
        return redis
        
    except Exception as e:
        logger.error("Redis connection failed", error=str(e))
        raise
        
class RedisManager:
    def __init__(self, redis_pool: aioredis.Redis):
        self.redis = redis_pool
        
    async def get_or_set(self, 
                        key: str, 
                        value_func, 
                        expire: Optional[int] = None):
        """Get value from cache or compute and store it."""
        value = await self.redis.get(key)
        
        if value is None:
            value = await value_func()
            if value is not None:
                await self.redis.set(key, value, ex=expire)
                
        return value
        
    async def cache_clear(self, pattern: str):
        """Clear cache entries matching pattern."""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
                logger.info(f"Cleared {len(keys)} cache entries")
        except Exception as e:
            logger.error("Cache clear failed", error=str(e))