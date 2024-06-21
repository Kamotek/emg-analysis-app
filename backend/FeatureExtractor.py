from abc import abstractmethod, ABC

import pandas as pd


class FeatureExtractor(ABC):
    @abstractmethod
    def extract(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
