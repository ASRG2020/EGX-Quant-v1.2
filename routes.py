from fastapi import APIRouter, HTTPException, Query
from app.data.provider import get_provider
from app.features.technical import add_technical_features
from app.signals.engine import score_signal
from app.backtest.engine import run_backtest, BacktestConfig
from config.settings import settings

router=APIRouter(prefix="/api/v1")
provider=get_provider()

def prepared(symbol, limit):
    df=provider.get_prices(symbol, limit=limit)
    return add_technical_features(df)

@router.get("/prices/{symbol}")
def prices(symbol: str, limit: int=Query(200, ge=50, le=5000)):
    try: return prepared(symbol,limit).tail(limit).to_dict(orient="records")
    except Exception as e: raise HTTPException(502,str(e))

@router.get("/signal/{symbol}")
def signal(symbol: str, limit: int=Query(300, ge=60, le=5000)):
    try:
        df=prepared(symbol,limit); s=score_signal(df)
        return {"symbol":symbol.upper(),"timestamp":df.date.iloc[-1].isoformat(),"close":float(df.close.iloc[-1]),**s}
    except Exception as e: raise HTTPException(502,str(e))

@router.get("/backtest/{symbol}")
def backtest(symbol: str, limit: int=Query(1000, ge=100, le=5000)):
    try:
        df=prepared(symbol,limit)
        df["signal"]=(df["sma20"]>df["sma50"]).astype(int)
        cfg=BacktestConfig(settings.initial_capital,settings.transaction_cost,settings.slippage)
        return {"symbol":symbol.upper(),**run_backtest(df,cfg)}
    except Exception as e: raise HTTPException(502,str(e))
