from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import requests
from config.settings import settings
from app.data.normalize import normalize_prices

class MarketDataProvider(ABC):
    @abstractmethod
    def get_prices(self, symbol: str, limit: int = 500) -> pd.DataFrame: ...

class DemoProvider(MarketDataProvider):
    def get_prices(self, symbol: str, limit: int = 500) -> pd.DataFrame:
        rng = np.random.default_rng(abs(hash(symbol.upper())) % (2**32))
        n = max(120, min(limit, 2000))
        ret = rng.normal(0.0005, 0.018, n)
        close = 100 * np.exp(np.cumsum(ret))
        dates = pd.date_range(end=pd.Timestamp.now(tz="UTC"), periods=n, freq="B")
        close_s = pd.Series(close)
        return pd.DataFrame({"date": dates, "symbol": symbol.upper(), "open": close_s.shift(1).fillna(close_s), "high": close_s * 1.01, "low": close_s * 0.99, "close": close_s, "volume": rng.integers(100000, 2000000, n)})

class RestProvider(MarketDataProvider):
    def __init__(self):
        if not settings.egx_api_url_template:
            raise RuntimeError("EGX_API_URL_TEMPLATE is not configured")
    def get_prices(self, symbol: str, limit: int = 500) -> pd.DataFrame:
        url = settings.egx_api_url_template.format(symbol=symbol.upper())
        headers = {}
        if settings.egx_api_key:
            headers[settings.egx_api_auth_header] = settings.egx_api_key
        r = requests.get(url, params={"limit": limit}, headers=headers, timeout=15)
        r.raise_for_status()
        payload = r.json()
        rows = payload.get("data", payload) if isinstance(payload, dict) else payload
        return normalize_prices(pd.DataFrame(rows), symbol)

def get_provider() -> MarketDataProvider:
    if settings.data_provider == "rest":
        return RestProvider()
    return DemoProvider()
