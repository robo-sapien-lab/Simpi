"""
Webhook notification utilities for Slack and Discord.
"""
import aiohttp
import json
import structlog
from typing import Optional, Dict, Any

logger = structlog.get_logger()

class WebhookNotifier:
    def __init__(self, 
                 slack_webhook_url: Optional[str] = None,
                 discord_webhook_url: Optional[str] = None):
        self.slack_url = slack_webhook_url
        self.discord_url = discord_webhook_url
        
    async def send_slack_notification(self, 
                                    message: str, 
                                    metadata: Optional[Dict] = None):
        """Send notification to Slack."""
        if not self.slack_url:
            return
            
        try:
            payload = {
                "text": message,
                "attachments": [{
                    "fields": [
                        {"title": k, "value": str(v), "short": True}
                        for k, v in (metadata or {}).items()
                    ]
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.slack_url,
                    json=payload
                ) as response:
                    if response.status != 200:
                        logger.error(
                            "Slack notification failed",
                            status=response.status
                        )
                        
        except Exception as e:
            logger.error("Slack notification error", error=str(e))
            
    async def send_discord_notification(self, 
                                      message: str,
                                      metadata: Optional[Dict] = None):
        """Send notification to Discord."""
        if not self.discord_url:
            return
            
        try:
            embed = {
                "title": "Bot Notification",
                "description": message,
                "fields": [
                    {"name": k, "value": str(v), "inline": True}
                    for k, v in (metadata or {}).items()
                ]
            }
            
            payload = {
                "embeds": [embed]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.discord_url,
                    json=payload
                ) as response:
                    if response.status != 204:
                        logger.error(
                            "Discord notification failed",
                            status=response.status
                        )
                        
        except Exception as e:
            logger.error("Discord notification error", error=str(e))