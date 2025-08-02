"""
Plugin for handling programming-related questions.
"""
from typing import Optional, List
import re
from plugins.base import BasePlugin

class LearnProgrammingPlugin(BasePlugin):
    name = "learn_programming"
    
    def __init__(self):
        self.programming_keywords = {
            'python', 'javascript', 'java', 'c++', 'code',
            'programming', 'function', 'class', 'algorithm'
        }
        
    async def can_handle(self, message: str) -> bool:
        """Check if message contains programming-related keywords."""
        message = message.lower()
        return any(keyword in message 
                  for keyword in self.programming_keywords)
                  
    async def handle_message(self, message: str) -> Optional[str]:
        """Handle programming-related questions."""
        # Detect programming language
        language = self._detect_language(message)
        
        # Detect question type
        if 'error' in message.lower():
            return await self._handle_error_question(message, language)
        elif 'how' in message.lower():
            return await self._handle_how_to_question(message, language)
        
        # Default response
        return await self._generate_programming_response(message, language)
        
    def _detect_language(self, message: str) -> Optional[str]:
        """Detect programming language from message."""
        message = message.lower()
        languages = {
            'python': r'\b(python|py)\b',
            'javascript': r'\b(javascript|js)\b',
            'java': r'\bjava\b',
            'c++': r'\b(c\+\+|cpp)\b'
        }
        
        for lang, pattern in languages.items():
            if re.search(pattern, message):
                return lang
        return None
        
    async def _handle_error_question(self, 
                                   message: str, 
                                   language: Optional[str]) -> str:
        """Handle error-related questions."""
        # TODO: Implement error handling logic
        return (f"I see you're having an error in {language}. "
                "Could you share the error message?")
                
    async def _handle_how_to_question(self, 
                                    message: str, 
                                    language: Optional[str]) -> str:
        """Handle how-to questions."""
        # TODO: Implement how-to guidance
        return (f"I can help you learn how to do that in {language}. "
                "Let me break it down...")
                
    async def _generate_programming_response(self, 
                                          message: str, 
                                          language: Optional[str]) -> str:
        """Generate a general programming-related response."""
        # TODO: Implement Venice API call for programming help
        return "I'll help you with your programming question..."