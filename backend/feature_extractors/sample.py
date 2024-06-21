import pandas as pd

from backend.FeatureExtractor import FeatureExtractor


class Sample(FeatureExtractor):
    def __init__(self):
        self.feature = 2137  # calculated by a complex algorithm based on the input data

    def extract(self, data):
        return pd.DataFrame(self.feature)
