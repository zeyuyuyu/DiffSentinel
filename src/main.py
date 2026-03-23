import numpy as np
from transformers import pipeline

class DiffSentinel:
    def __init__(self):
        self.sentiment_analyzer = pipeline('sentiment-analysis')

    def analyze_sentiment_diff(self, text1, text2):
        """
        Performs differential sentiment analysis between two input texts.
        
        Args:
            text1 (str): The first text to analyze.
            text2 (str): The second text to analyze.
        
        Returns:
            dict: A dictionary containing the sentiment difference, with keys 'score_diff' and 'label_diff'.
        """
        sentiment1 = self.sentiment_analyzer(text1)[0]
        sentiment2 = self.sentiment_analyzer(text2)[0]
        
        score_diff = sentiment2['score'] - sentiment1['score']
        label_diff = sentiment2['label'] - sentiment1['label']
        
        return {'score_diff': score_diff, 'label_diff': label_diff}
