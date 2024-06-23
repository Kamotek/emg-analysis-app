import pandas as pd

from backend.filter import Filter


class Sample(Filter):
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
