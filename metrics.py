import numpy as np
import pandas as pd

def performance_metrics(r: pd.Series) -> dict:
    r = r.dropna()
    if r.empty: return {"total_return":0.0,"annualized_return":0.0,"volatility":0.0,"sharpe":0.0,"max_drawdown":0.0}
    eq=(1+r).cumprod(); total=float(eq.iloc[-1]-1)
    ann=float(eq.iloc[-1]**(252/len(r))-1) if len(r)>0 else 0.0
    vol=float(r.std(ddof=1)*np.sqrt(252)) if len(r)>1 else 0.0
    sharpe=float(r.mean()/r.std(ddof=1)*np.sqrt(252)) if len(r)>1 and r.std(ddof=1)!=0 else 0.0
    dd=eq/eq.cummax()-1
    return {"total_return":total,"annualized_return":ann,"volatility":vol,"sharpe":sharpe,"max_drawdown":float(dd.min())}
