# EGX Quant V1.2

A modular quantitative research and market-monitoring platform for Egyptian Exchange (EGX) equities.

## What it does
- Normalizes OHLCV market data.
- Computes technical features (SMA, EMA, RSI, MACD, ATR, Bollinger Bands, momentum, volume features).
- Produces a transparent BUY/HOLD/SELL research signal with score and confidence.
- Provides an ML-ready time-series model interface and a Random Forest baseline.
- Runs leakage-aware backtests with transaction costs and slippage.
- Reports return, volatility, Sharpe, drawdown, win rate and benchmark-relative alpha.
- Exposes a FastAPI service for prices, signals and backtests.

## Important limitation
The repository contains no secret keys and no proprietary EGX feed. For live/intraday operation, configure an authorized data provider through environment variables. EGID states that it is a fully owned EGX subsidiary and an authorized EGX market-data provider; ICE also lists EGX real-time/delayed/EOD/historical data through its data products. The application therefore keeps the data-provider layer replaceable rather than embedding an undocumented endpoint.

Synthetic data is only a development fallback and must never be presented as real EGX data.

## Quick start

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.api.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Example endpoints

- `GET /health`
- `GET /api/v1/prices/COMI?limit=200`
- `GET /api/v1/signal/COMI`
- `GET /api/v1/backtest/COMI`

## Live data configuration

The code supports a generic REST provider using:

- `DATA_PROVIDER=rest`
- `EGX_API_URL_TEMPLATE=https://your-provider.example/v1/bars/{symbol}`
- `EGX_API_KEY=...`

The exact URL, headers and JSON mapping must match the provider's official API contract. Do not guess or scrape a provider endpoint.

## Methodology

The baseline signal uses multiple independent feature groups. Backtests shift the position by one bar to avoid look-ahead bias, and costs/slippage are configurable. ML evaluation uses chronological splits rather than random shuffling.

## Disclaimer

This is research/educational software. Model outputs are probabilistic signals, not guarantees or personalized financial advice. Never rely on a model without validating the data, execution assumptions, and out-of-sample performance.
