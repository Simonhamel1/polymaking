"""Base de stratégie pour le market making.

Ce module définit les structures minimales pour concevoir des stratégies
de quotation. Les implémentations concrètes doivent hériter de `Strategy`
et retourner une liste de `Quote` pertinentes.
"""

from dataclasses import dataclass
from typing import List

from ..constants import Side


@dataclass
class Quote:
    """Une proposition d'ordre limite.

    Champs:
    - side: Side.BUY ou Side.SELL.
    - price: prix limite proposé.
    - size: quantité souhaitée.
    """
    side: Side
    price: float
    size: float


class Strategy:
    """Interface de base pour les stratégies de market making.

    Les sous-classes doivent implémenter `generate_quotes`, en tenant compte
    au minimum du prix mid et de l'inventaire courant.
    """

    def generate_quotes(self, mid_price: float, inventory: float) -> List[Quote]:
        """Génère des quotes (bid/ask) à partir de l'état courant.

        Args:
            mid_price: prix mid actuel du marché.
            inventory: inventaire détenu par le maker.

        Returns:
            Liste de `Quote` à publier.
        """
        raise NotImplementedError
