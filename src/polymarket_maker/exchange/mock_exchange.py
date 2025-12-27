import random
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Order:
    id: str
    side: str  # "buy" or "sell"
    price: float
    size: float
    timestamp: float


class MockExchange:
    """
    Échange simulé pour la démo:
    - Prix mid évolue par marche aléatoire autour d'un centre.
    - Ordres placés peuvent se remplir avec une probabilité selon distance au mid.
    - Suit inventaire et cash; calcule une PnL mark-to-market.
    """

    def __init__(self, start_mid: float = 0.5, volatility: float = 0.01) -> None:
        self.mid_price = start_mid
        self.volatility = volatility
        self.inventory = 0.0
        self.cash = 0.0
        self.open_orders: List[Order] = []
        self.last_order_id = 0

    def _gen_order_id(self) -> str:
        self.last_order_id += 1
        return f"MOCK-{self.last_order_id}"

    def get_mid_price(self) -> float:
        return self.mid_price

    def tick(self) -> None:
        # Random walk, borné dans [0.05, 0.95] pour binary-style pricing
        drift = random.gauss(0, self.volatility)
        self.mid_price = max(0.05, min(0.95, self.mid_price + drift))
        # Simuler des fills
        self._maybe_fill_orders()

    def place_order(self, side: str, price: float, size: float) -> str:
        oid = self._gen_order_id()
        self.open_orders.append(Order(oid, side, price, size, time.time()))
        return oid

    def cancel_all(self) -> None:
        self.open_orders.clear()

    def _maybe_fill_orders(self) -> None:
        filled: List[Order] = []
        for o in self.open_orders:
            # Plus l'ordre est proche du mid, plus il a de chances d'être rempli
            distance = abs(o.price - self.mid_price)
            base_prob = 0.3
            prob = max(0.05, base_prob - distance)  # loin du mid -> prob plus faible
            if random.random() < prob:
                filled.append(o)
        # Appliquer fills
        for o in filled:
            if o.side == "buy":
                self.inventory += o.size
                self.cash -= o.size * o.price
            else:
                self.inventory -= o.size
                self.cash += o.size * o.price
            self.open_orders.remove(o)

    def mark_to_market_pnl(self) -> float:
        # Valeur mark-to-market: cash + inventaire à mid
        return self.cash + self.inventory * self.mid_price

    def status(self) -> dict:
        return {
            "mid": self.mid_price,
            "inventory": self.inventory,
            "cash": self.cash,
            "pnl": self.mark_to_market_pnl(),
            "open_orders": len(self.open_orders),
        }
