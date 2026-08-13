import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    data_provider: str = os.getenv("DATA_PROVIDER", "demo").lower()
    egx_api_url_template: str = os.getenv("EGX_API_URL_TEMPLATE", "")
    egx_api_key: str = os.getenv("EGX_API_KEY", "")
    egx_api_auth_header: str = os.getenv("EGX_API_AUTH_HEADER", "X-API-Key")
    initial_capital: float = float(os.getenv("INITIAL_CAPITAL", "100000"))
    transaction_cost: float = float(os.getenv("TRANSACTION_COST", "0.001"))
    slippage: float = float(os.getenv("SLIPPAGE", "0.0005"))

settings = Settings()
