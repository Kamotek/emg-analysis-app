import pandas as pd

from backend.Filter import Filter


class Sample(Filter):
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
