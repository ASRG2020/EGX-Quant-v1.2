import pandas as pd
from app.features.technical import add_technical_features

def test_features():
    n=100; c=pd.Series(range(1,n+1),dtype=float)
    df=pd.DataFrame({"date":pd.date_range("2025-01-01",periods=n),"symbol":"TEST","open":c,"high":c*1.01,"low":c*.99,"close":c,"volume":1000})
    out=add_technical_features(df)
    for col in ["sma20","sma50","rsi14","macd","atr14","bb_upper","momentum20","volume_ratio"]: assert col in out
