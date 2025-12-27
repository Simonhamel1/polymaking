from typing import List

from .base import Quote, Strategy


class ConstantSpreadStrategy(Strategy):
    def __init__(self, spread_bps: float, quote_size: float) -> None:
        self.spread = float(spread_bps) / 10_000.0
        self.size = quote_size

    def generate_quotes(self, mid_price: float, inventory: float) -> List[Quote]:
        bid = max(0.01, mid_price * (1.0 - self.spread))
        ask = min(0.99, mid_price * (1.0 + self.spread))
        return [
            Quote("buy", round(bid, 4), self.size),
            Quote("sell", round(ask, 4), self.size),
        ]
