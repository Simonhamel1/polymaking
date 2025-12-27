from dataclasses import dataclass
from typing import Optional
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


@dataclass
class AppConfig:
    mode: str = "demo"  # 'demo' or 'live'
    market_id: Optional[str] = None
    spread_bps: float = 50.0  # 0.50%
    quote_size: float = 100.0
    inventory_limit: float = 1000.0
    refresh_seconds: float = 1.0
    use_mock: bool = True
    api_base: str = "https://api.polymarket.com"


def _get_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default


def load_config() -> AppConfig:
    return AppConfig(
        mode=os.getenv("PM_MODE", "demo"),
        market_id=os.getenv("PM_MARKET_ID") or None,
        spread_bps=_get_float("PM_SPREAD_BPS", 50.0),
        quote_size=_get_float("PM_QUOTE_SIZE", 100.0),
        inventory_limit=_get_float("PM_INVENTORY_LIMIT", 1000.0),
        refresh_seconds=_get_float("PM_REFRESH_SECONDS", 1.0),
        use_mock=os.getenv("PM_USE_MOCK", "true").lower() in ("1", "true", "yes"),
        api_base=os.getenv("PM_API_BASE", "https://api.polymarket.com"),
    )
