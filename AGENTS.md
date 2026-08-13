# EGX Quant V1.2 Agent Instructions

## Mission
Build a modular quantitative research and market-monitoring platform for EGX equities.

## Rules
- Keep data ingestion, normalization, features, models, signals, backtesting and API layers separate.
- Synthetic data is only for tests/development; never label it as EGX data.
- Never hard-code API keys, tokens, cookies or private credentials.
- Never invent an undocumented provider endpoint.
- Avoid look-ahead bias: predictions/signals for bar t must only use information available at or before t and trades should be executed according to an explicit next-bar/execution assumption.
- Use chronological or walk-forward validation for time series.
- Compare strategies with Buy & Hold and, when available, an appropriate EGX benchmark.
- Report assumptions, costs, slippage, missing data and sample periods.
- Do not claim alpha unless it is reproducible out-of-sample and benchmark-relative.
- Run `pytest -q` after code changes.
- Keep API responses JSON serializable.
