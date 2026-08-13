from abc import ABC, abstractmethod
import pandas as pd

class SignalModel(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series): ...
    @abstractmethod
    def predict(self, X: pd.DataFrame): ...
