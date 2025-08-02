"""
Analytics and metrics tracking system.
"""
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta
import asyncio
import json
import structlog
from dataclasses import dataclass

logger = structlog.get_logger()

dataclass
class Interaction:
    timestamp: float
    user_id: str
    prompt: str
    response: str
    response_time: float
    upvotes: int = 0
    sentiment_score: float = 0.0

class AnalyticsEngine:
    def __init__(self, redis_pool):
        self.redis = redis_pool
        self.current_interactions: List[Interaction] = []
        self.trending_topics: Dict[str, int] = {}
        
        # Start background tasks
        self.tasks = [
            asyncio.create_task(self._persist_metrics()),
            asyncio.create_task(self._analyze_trends())
        ]
        
    async def log_interaction(self, 
                            user_id: str, 
                            prompt: str, 
                            response: str, 
                            response_time: Optional[float] = None):
        """Log a single bot interaction."""
        interaction = Interaction(
            timestamp=time.time(),
            user_id=user_id,
            prompt=prompt,
            response=response,
            response_time=response_time or 0.0
        )
        
        self.current_interactions.append(interaction)
        await self._update_metrics(interaction)
        
    async def _update_metrics(self, interaction: Interaction):
        """Update real-time metrics."""
        # Update response time metrics
        await self.redis.hincrby(
            'metrics:response_times',
            interaction.user_id,
            interaction.response_time
        )
        
        # Update user interaction count
        await self.redis.hincrby(
            'metrics:user_interactions',
            interaction.user_id,
            1
        )
        
    async def _persist_metrics(self):
        """Periodically persist metrics to storage."""
        while True:
            try:
                if self.current_interactions:
                    # Batch write interactions
                    await self.redis.rpush(
                        'analytics:interactions',
                        *[
                            json.dumps(vars(i)) 
                            for i in self.current_interactions
                        ]
                    )
                    
                    self.current_interactions.clear()
                    
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error("Error persisting metrics", error=str(e))
                await asyncio.sleep(60)
                
    async def _analyze_trends(self):
        """Analyze trending topics periodically."""
        while True:
            try:
                # Get recent interactions
                raw_interactions = await self.redis.lrange(
                    'analytics:interactions',
                    -1000,  # Last 1000 interactions
                    -1
                )
                
                topics = {}
                for raw in raw_interactions:
                    interaction = json.loads(raw)
                    # Simple word frequency analysis
                    words = interaction['prompt'].lower().split()
                    for word in words:
                        if len(word) > 3:  # Skip short words
                            topics[word] = topics.get(word, 0) + 1
                            
                # Update trending topics
                self.trending_topics = dict(
                    sorted(
                        topics.items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:10]
                )
                
                await asyncio.sleep(3600)  # 1 hour
                
            except Exception as e:
                logger.error("Error analyzing trends", error=str(e))
                await asyncio.sleep(300)
                
    async def get_user_metrics(self, user_id: str) -> Dict:
        """Get metrics for a specific user."""
        response_times = await self.redis.hget(
            'metrics:response_times',
            user_id
        )
        interaction_count = await self.redis.hget(
            'metrics:user_interactions',
            user_id
        )
        
        return {
            'response_times': float(response_times or 0),
            'interaction_count': int(interaction_count or 0)
        }
        
    async def get_trending_topics(self) -> Dict[str, int]:
        """Get current trending topics."""
        return self.trending_topics
