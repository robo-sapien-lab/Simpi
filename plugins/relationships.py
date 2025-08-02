"""
Plugin for handling relationship advice questions.
"""
from typing import Optional
import re
from plugins.base import BasePlugin

class RelationshipsPlugin(BasePlugin):
    name = "relationships"
    
    def __init__(self):
        self.relationship_keywords = {
            'relationship', 'dating', 'partner', 'marriage',
            'boyfriend', 'girlfriend', 'spouse', 'breakup'
        }
        
    async def can_handle(self, message: str) -> bool:
        """Check if message is relationship-related."""
        message = message.lower()
        return any(keyword in message 
                  for keyword in self.relationship_keywords)
                  
    async def handle_message(self, message: str) -> Optional[str]:
        """Handle relationship advice requests."""
        message_type = self._categorize_message(message)
        
        if message_type == 'crisis':
            return self._handle_crisis()
        elif message_type == 'advice':
            return await self._generate_advice(message)
        else:
            return await self._generate_general_response(message)
            
    def _categorize_message(self, message: str) -> str:
        """Categorize the type of relationship question."""
        message = message.lower()
        
        crisis_keywords = {'suicide', 'hurt', 'abuse', 'violence'}
        if any(word in message for word in crisis_keywords):
            return 'crisis'
            
        advice_keywords = {'should i', 'what should', 'how do i'}
        if any(phrase in message for phrase in advice_keywords):
            return 'advice'
            
        return 'general'
        
    def _handle_crisis(self) -> str:
        """Handle crisis situations with appropriate resources."""
        return (
            "I notice this might be a serious situation. "
            "Please remember:\n\n"
            "1. Your safety is the top priority\n"
            "2. Contact emergency services if you're in danger\n"
            "3. National Crisis Hotline: 988\n"
            "4. Consider speaking with a professional counselor\n\n"
            "Would you like me to provide more specific resources?"
        )
        
    async def _generate_advice(self, message: str) -> str:
        """Generate relationship advice based on the question."""
        # TODO: Implement Venice API call for relationship advice
        return ("I understand you're looking for relationship advice. "
                "Let me help you think through this...")
                
    async def _generate_general_response(self, message: str) -> str:
        """Generate a general response for relationship topics."""
        # TODO: Implement Venice API call for general response
        return ("I hear you talking about your relationship. "
                "Would you like to tell me more about the situation?")