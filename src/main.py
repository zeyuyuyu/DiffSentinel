import numpy as np
from transformers import pipeline

class DiffSentinel:
    def __init__(self):
        self.anomaly_detector = pipeline('text-classification', model='roberta-base-anomaly-detector')

    def detect_anomalies(self, text_input):
        """
        Detects anomalies in the provided text input using a pre-trained RoBERTa model.
        
        Args:
            text_input (str): The text to analyze for anomalies.
        
        Returns:
            dict: A dictionary containing the anomaly score and classification label.
        """
        result = self.anomaly_detector(text_input)
        return {
            'anomaly_score': result[0]['score'],
            'label': result[0]['label']
        }

if __name__ == '__main__':
    sentinel = DiffSentinel()
    text = "This is a normal input."
    anomaly_result = sentinel.detect_anomalies(text)
    print(anomaly_result)
