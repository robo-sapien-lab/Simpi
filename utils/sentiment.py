"""
Sentiment analysis utilities using VADER.
"""
from typing import Dict, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Analyze text sentiment and return score and category.
        
        Returns:
            Tuple of (compound_score, category)
            where category is one of: positive, negative, neutral
        """
        scores = self.analyzer.polarity_scores(text)
        
        # Get compound score
        compound = scores['compound']
        
        # Determine category
        if compound >= 0.05:
            category = 'positive'
        elif compound <= -0.05:
            category = 'negative'
        else:
            category = 'neutral'
            
        return compound, category
        
    def get_detailed_metrics(self, text: str) -> Dict[str, float]:
        """Get detailed sentiment metrics."""
        return self.analyzer.polarity_scores(text)