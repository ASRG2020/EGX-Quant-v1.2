import numpy as np
import pandas as pd

def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    c = out["close"]
    h, l = out["high"], out["low"]
    out["return_1d"] = c.pct_change()
    out["sma20"] = c.rolling(20).mean()
    out["sma50"] = c.rolling(50).mean()
    out["ema12"] = c.ewm(span=12, adjust=False).mean()
    out["ema26"] = c.ewm(span=26, adjust=False).mean()
    out["macd"] = out["ema12"] - out["ema26"]
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    out["rsi14"] = 100 - 100 / (1 + rs)
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    out["atr14"] = tr.rolling(14).mean()
    mid = c.rolling(20).mean(); std = c.rolling(20).std()
    out["bb_mid"] = mid; out["bb_upper"] = mid + 2*std; out["bb_lower"] = mid - 2*std
    out["momentum20"] = c / c.shift(20) - 1
    out["volume_sma20"] = out["volume"].rolling(20).mean()
    out["volume_ratio"] = out["volume"] / out["volume_sma20"].replace(0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)
