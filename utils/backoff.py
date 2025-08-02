"""
Exponential backoff decorator for rate-limited operations.
"""
import asyncio
import functools
import random
from typing import Callable, Any
import structlog

logger = structlog.get_logger()

def exponential_backoff(
    start_delay: float = 1.0,
    max_delay: float = 60.0,
    max_retries: int = 5
):
    """
    Decorator for exponential backoff retry logic.
    
    Args:
        start_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        max_retries: Maximum number of retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = start_delay
            retries = 0
            
            while True:
                try:
                    return await func(*args, **kwargs)
                    
                except Exception as e:
                    retries += 1
                    
                    if retries >= max_retries:
                        logger.error(
                            "Max retries exceeded",
                            function=func.__name__,
                            error=str(e)
                        )
                        raise
                        
                    # Calculate next delay with jitter
                    jitter = random.uniform(0.8, 1.2)
                    next_delay = min(delay * 2 * jitter, max_delay)
                    
                    logger.warning(
                        "Operation failed, retrying",
                        function=func.__name__,
                        retry_count=retries,
                        delay=next_delay,
                        error=str(e)
                    )
                    
                    await asyncio.sleep(next_delay)
                    delay = next_delay
                    
        return wrapper
    return decorator
