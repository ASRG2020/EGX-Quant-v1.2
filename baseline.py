import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit

FEATURES = ["return_1d","sma20","sma50","ema12","ema26","macd","macd_signal","rsi14","atr14","bb_mid","bb_upper","bb_lower","momentum20","volume_ratio"]

class RFTimeSeriesModel:
    def __init__(self, n_estimators=300, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, class_weight="balanced_subsample", min_samples_leaf=5)
    def fit(self, X, y):
        self.model.fit(X[FEATURES].ffill().bfill(), y)
        return self
    def predict_proba(self, X):
        return self.model.predict_proba(X[FEATURES].ffill().bfill())

def make_target(df: pd.DataFrame, horizon: int = 1, threshold: float = 0.002) -> pd.Series:
    fwd = df["close"].shift(-horizon) / df["close"] - 1
    return pd.Series((fwd > threshold).astype(int), index=df.index).where(fwd.notna())

def chronological_split(df, frac=0.8):
    n = int(len(df)*frac)
    return df.iloc[:n].copy(), df.iloc[n:].copy()
