#!/usr/bin/env python3
"""
Simpi Singh - Main Entry Point
Initializes and runs the Reddit bot with all its components.
"""
import asyncio
import os
from dotenv import load_dotenv
import structlog
from bot.bot import SimpiBot
from config.settings import load_settings
from utils.redis_client import init_redis_pool

# Configure structured logging
logger = structlog.get_logger()


async def main():
    """Initialize and run the Simpi bot."""
    try:
        # Load environment variables
        load_dotenv()

        # Load configuration
        settings = load_settings()

        # Initialize Redis connection
        redis_pool = await init_redis_pool(os.getenv('REDIS_URL'))

        # Create and start bot instance
        bot = SimpiBot(settings, redis_pool)
        await bot.start()

        # Keep the bot running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down Simpi bot...")
        await bot.shutdown()
    except Exception as e:
        logger.error("Fatal error", error=str(e))
        raise


if __name__ == "__main__":
    asyncio.run(main())
