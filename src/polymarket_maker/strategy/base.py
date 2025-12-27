from dataclasses import dataclass
from typing import List


@dataclass
class Quote:
    side: str  # "buy" or "sell"
    price: float
    size: float


class Strategy:
    def generate_quotes(self, mid_price: float, inventory: float) -> List[Quote]:
        raise NotImplementedError
