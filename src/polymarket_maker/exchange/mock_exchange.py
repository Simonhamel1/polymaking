"""Mock d'échange pour la démo Polymarket.

Ce module fournit un échange simulé utile pour tester la boucle de market making
sans dépendre d'une API live.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict, Any

from ..constants import Side
from .base import Exchange


@dataclass
class Order:
    """Représente un ordre limite simulé."""
    id: str
    side: Side
    price: float
    size: float
    timestamp: float


class MockExchange(Exchange):
    """Échange simulé minimaliste pour la démo.

    Implémente l'interface Exchange standard.
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
        """Avance la simulation (marche aléatoire + fills)."""
        # Marche aléatoire
        drift = random.gauss(0, self.volatility)
        self.mid_price = max(0.05, min(0.95, self.mid_price + drift))
        # Fills
        self._maybe_fill_orders()

    def place_order(self, side: Side, price: float, size: float) -> str:
        oid = self._gen_order_id()
        self.open_orders.append(Order(oid, side, price, size, time.time()))
        return oid

    def cancel_all(self) -> None:
        self.open_orders.clear()

    def get_portfolio(self) -> Dict[str, float]:
        """Retourne l'état standardisé."""
        return {
            "inventory": self.inventory,
            "cash": self.cash,
            "pnl": self.mark_to_market_pnl(),
            # Extra info (non standard mais utile pour debug/demo)
            "open_orders_count": len(self.open_orders),
            "mid": self.mid_price
        }

    def _maybe_fill_orders(self) -> None:
        """Logique interne de fill probabiliste."""
        filled: List[Order] = []
        for o in self.open_orders:
            distance = abs(o.price - self.mid_price)
            base_prob = 0.3
            prob = max(0.05, base_prob - distance)
            if random.random() < prob:
                filled.append(o)
        
        for o in filled:
            if o.side == Side.BUY:
                self.inventory += o.size
                self.cash -= o.size * o.price
            else:
                self.inventory -= o.size
                self.cash += o.size * o.price
            self.open_orders.remove(o)

    def mark_to_market_pnl(self) -> float:
        return self.cash + self.inventory * self.mid_price