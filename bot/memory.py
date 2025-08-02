"""
Memory management system for storing and retrieving user context.
"""
from typing import Dict, List, Optional
import json
import time
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()

dataclass
class UserPreference:
    topic_interests: List[str]
    expertise_level: str
    preferred_tone: str
    last_updated: float

dataclass
class FAQ:
    question: str
    answer: str
    created_at: float
    uses: int

class MemoryManager:
    def __init__(self, redis_pool):
        self.redis = redis_pool
        
    async def get_context(self, user_id: str) -> Dict:
        """Get full context for a user."""
        try:
            context = {
                'preferences': await self._get_preferences(user_id),
                'faqs': await self._get_faqs(user_id),
                'recent_interactions': await self._get_recent_interactions(user_id)
            }
            return context
        except Exception as e:
            logger.error("Error getting context", 
                        error=str(e), 
                        user_id=user_id)
            return {}
            
    async def _get_preferences(self, user_id: str) -> Optional[UserPreference]:
        """Get user preferences from Redis."""
        data = await self.redis.get(f'prefs:{user_id}')
        if data:
            data = json.loads(data)
            return UserPreference(**data)
        return None
        
    async def _get_faqs(self, user_id: str) -> List[FAQ]:
        """Get user's saved FAQs."""
        faqs = []
        raw_faqs = await self.redis.lrange(f'faqs:{user_id}', 0, -1)
        for raw in raw_faqs:
            data = json.loads(raw)
            faqs.append(FAQ(**data))
        return faqs
        
    async def _get_recent_interactions(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get recent interactions for context."""
        interactions = []
        raw_interactions = await self.redis.lrange(
            f'interactions:{user_id}',
            -limit,
            -1
        )
        for raw in raw_interactions:
            interactions.append(json.loads(raw))
        return interactions
        
    async def update_preferences(self, 
                               user_id: str, 
                               preferences: UserPreference):
        """Update user preferences."""
        try:
            await self.redis.set(
                f'prefs:{user_id}',
                json.dumps(vars(preferences))
            )
        except Exception as e:
            logger.error("Error updating preferences", 
                        error=str(e), 
                        user_id=user_id)
            
    async def save_faq(self, user_id: str, question: str, answer: str):
        """Save a new FAQ for the user."""
        faq = FAQ(
            question=question,
            answer=answer,
            created_at=time.time(),
            uses=0
        )
        
        try:
            await self.redis.rpush(
                f'faqs:{user_id}',
                json.dumps(vars(faq))
            )
        except Exception as e:
            logger.error("Error saving FAQ", 
                        error=str(e), 
                        user_id=user_id)
            
    async def log_interaction(self, user_id: str, interaction: Dict):
        """Log a new interaction for the user."""
        try:
            await self.redis.rpush(
                f'interactions:{user_id}',
                json.dumps(interaction)
            )
            # Trim to last 100 interactions
            await self.redis.ltrim(f'interactions:{user_id}', -100, -1)
        except Exception as e:
            logger.error("Error logging interaction", 
                        error=str(e), 
                        user_id=user_id)