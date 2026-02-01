from typing import List

from ..constants import Side
from .base import Quote, Strategy


class ConstantSpreadStrategy(Strategy):
    """Stratégie simple à spread constant autour du mid.

    Paramètres:
        spread_bps: écart en basis points (bps), p.ex. 50 bps => 0.50%.
        quote_size: taille des quotes (quantité constante).
    """

    def __init__(self, spread_bps: float, quote_size: float) -> None:
        self.spread = float(spread_bps) / 10_000.0
        self.size = quote_size

    def generate_quotes(self, mid_price: float, inventory: float) -> List[Quote]:
        """Génère un bid et un ask en appliquant le spread au mid.

        On applique des bornes (0.01, 0.99) pour éviter des quotes trop
        extrêmes dans un contexte binaire.
        """
        bid = max(0.01, mid_price * (1.0 - self.spread))
        ask = min(0.99, mid_price * (1.0 + self.spread))
        return [
            Quote(Side.BUY, round(bid, 4), self.size),
            Quote(Side.SELL, round(ask, 4), self.size),
        ]
