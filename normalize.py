import pandas as pd

REQUIRED = ["date", "symbol", "open", "high", "low", "close", "volume"]

def normalize_prices(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=REQUIRED)
    out = df.copy()
    aliases = {c.lower().strip(): c for c in out.columns}
    rename = {}
    for target in REQUIRED:
        if target in out.columns:
            continue
        if target in aliases:
            rename[aliases[target]] = target
    out = out.rename(columns=rename)
    if "date" not in out.columns:
        raise ValueError("Provider response must contain a date/timestamp field")
    if "close" not in out.columns:
        raise ValueError("Provider response must contain close")
    for c in ["open", "high", "low"]:
        if c not in out.columns:
            out[c] = out["close"]
    if "volume" not in out.columns:
        out["volume"] = 0
    out["date"] = pd.to_datetime(out["date"], utc=True, errors="coerce")
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out["symbol"] = symbol.upper()
    out = out.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates("date")
    return out[REQUIRED].reset_index(drop=True)
