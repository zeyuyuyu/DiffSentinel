import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination=0.01):
        self.model = IsolationForest(contamination=contamination)

    def fit(self, X):
        self.model.fit(X)

    def detect(self, X):
        scores = self.model.decision_function(X)
        anomalies = scores < 0
        return anomalies

def main():
    # Load data
    data = np.loadtxt('data.csv', delimiter=',')

    # Initialize and train anomaly detector
    detector = AnomalyDetector()
    detector.fit(data)

    # Detect anomalies
    anomalies = detector.detect(data)
    print(f'Detected {np.sum(anomalies)} anomalies.')

if __name__ == '__main__':
    main()