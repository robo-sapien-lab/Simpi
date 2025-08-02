"""
Content moderation and safety control system.
"""
from typing import List, Dict, Set
import re
import asyncio
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()

dataclass
class ContentFlag:
    reason: str
    severity: int
    context: str

class ModerationSystem:
    def __init__(self):
        self.blocked_patterns: Set[str] = set()
        self.spam_threshold = 5
        self.user_message_count: Dict[str, int] = {}
        self.flagged_content: Dict[str, List[ContentFlag]] = {}
        
        # Load blocked patterns
        self._load_patterns()
        
    def _load_patterns(self):
        """Load regex patterns for content filtering."""
        # Basic examples - extend with more comprehensive rules
        self.blocked_patterns = {
            r'\b(hate|abuse|violence)\b',
            r'(^|\s)spam(\s|$)',
            # Add more patterns as needed
        }
        
    async def check_message(self, content: str, user_id: str = None) -> bool:
        """Check if message content passes moderation rules.
        Returns True if content is safe, False if it should be blocked."""
        content = content.lower()
        
        # Check against blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, content):
                await self._flag_content(
                    user_id, 
                    "blocked_pattern", 
                    2, 
                    pattern
                )
                return False
                
        # Check for spam
        if user_id:
            if await self._check_spam(user_id):
                await self._flag_content(
                    user_id, 
                    "spam", 
                    1, 
                    "frequent_messages"
                )
                return False
                
        return True
        
    async def _check_spam(self, user_id: str) -> bool:
        """Check if user is spamming based on message frequency."""
        current_count = self.user_message_count.get(user_id, 0)
        self.user_message_count[user_id] = current_count + 1
        
        if current_count > self.spam_threshold:
            return True
            
        # Reset count after delay
        asyncio.create_task(self._reset_count(user_id))
        return False
        
    async def _reset_count(self, user_id: str):
        """Reset user's message count after delay."""
        await asyncio.sleep(60)  # 1 minute window
        self.user_message_count[user_id] = 0
        
    async def _flag_content(self, 
                          user_id: str, 
                          reason: str, 
                          severity: int, 
                          context: str):
        """Flag content for review."""
        if user_id not in self.flagged_content:
            self.flagged_content[user_id] = []
            
        flag = ContentFlag(reason, severity, context)
        self.flagged_content[user_id].append(flag)
        
        logger.warning(
            "Content flagged",
            user_id=user_id,
            reason=reason,
            severity=severity
        )
        
    async def get_flagged_content(self) -> Dict[str, List[ContentFlag]]:
        """Get all flagged content for review."""
        return self.flagged_content
