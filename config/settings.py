"""
Settings and configuration management for Simpi Singh bot.
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RedditSettings:
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = "SimpiSinghBot/1.0"

@dataclass
class VeniceSettings:
    api_key: str

@dataclass
class DatabaseSettings:
    redis_url: str
    postgres_url: Optional[str] = None

@dataclass
class WebhookSettings:
    slack_webhook_url: Optional[str] = None
    discord_webhook_url: Optional[str] = None

@dataclass
class Settings:
    reddit: RedditSettings
    venice: VeniceSettings
    database: DatabaseSettings
    webhooks: WebhookSettings
    log_level: str = "INFO"
    spam_threshold: int = 5
    response_timeout: int = 30
    max_retries: int = 3

def load_settings() -> Settings:
    return Settings(
        reddit=RedditSettings(
            client_id=os.getenv("REDDIT_CLIENT_ID", ""),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
            username=os.getenv("REDDIT_USERNAME", ""),
            password=os.getenv("REDDIT_PASSWORD", ""),
            user_agent=os.getenv("REDDIT_USER_AGENT", "SimpiSinghBot/1.0")
        ),
        venice=VeniceSettings(
            api_key=os.getenv("VENICE_API_KEY", "")
        ),
        database=DatabaseSettings(
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            postgres_url=os.getenv("POSTGRES_URL")
        ),
        webhooks=WebhookSettings(
            slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
            discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL")
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        spam_threshold=int(os.getenv("SPAM_THRESHOLD", "5")),
        response_timeout=int(os.getenv("RESPONSE_TIMEOUT", "30")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
    )
