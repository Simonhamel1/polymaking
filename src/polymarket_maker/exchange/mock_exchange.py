"""Mock d'échange pour la démo Polymarket.

Ce module fournit un échange simulé utile pour tester la boucle de market making
sans dépendre d'une API live. Les principales hypothèses sont:
- Le prix "mid" suit une marche aléatoire bornée dans [0.05, 0.95].
- Les ordres sont remplis de manière probabiliste en fonction de la proximité
  de leur prix au mid.
- L'inventaire et le cash sont mis à jour à chaque remplissage; le PnL est
  calculé en mark-to-market sur le mid courant.

Limites connues:
- Pas de carnet d'ordres ni de profondeur réelle.
- Pas de latence, pas de slippage autre que probabiliste.
- Les tailles et prix sont traités comme des flottants simples (unités arbitraires).
"""

import random
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Order:
    """Représente un ordre limite simulé.

    Champs:
    - id: identifiant unique généré par l'échange mock.
    - side: "buy" (achat) ou "sell" (vente).
    - price: prix limite de l'ordre (dans [0, 1] pour un marché binaire).
    - size: quantité (unités arbitraires, p.ex. contrats).
    - timestamp: époque UNIX au moment du placement.
    """

    id: str
    side: str  # "buy" ou "sell"
    price: float
    size: float
    timestamp: float


class MockExchange:
    """Échange simulé minimaliste pour la démo.

    Comportement:
    - Le mid évolue par marche aléatoire (volatilité réglable).
    - Les ordres ouverts peuvent se remplir aléatoirement, plus le prix est
      proche du mid, plus la probabilité de fill est élevée.
    - Maintient l'état: inventaire, cash, ordres ouverts; expose un PnL M2M.
    """

    def __init__(self, start_mid: float = 0.5, volatility: float = 0.01) -> None:
        """Initialise l'échange mock.

        Args:
            start_mid: mid de départ (par défaut 0.5).
            volatility: écart-type de la marche aléatoire par tick.
        """
        self.mid_price = start_mid
        self.volatility = volatility
        self.inventory = 0.0
        self.cash = 0.0
        self.open_orders: List[Order] = []
        self.last_order_id = 0

    def _gen_order_id(self) -> str:
        """Génère un identifiant d'ordre unique côté mock."""
        self.last_order_id += 1
        return f"MOCK-{self.last_order_id}"

    def get_mid_price(self) -> float:
        """Retourne le prix mid courant."""
        return self.mid_price

    def tick(self) -> None:
        """Avance d'un tick:

        - Met à jour le mid par marche aléatoire bornée.
        - Tente des remplissages probabilistes d'ordres ouverts.
        """
        # Marche aléatoire, bornée dans [0.05, 0.95] pour un pricing binaire
        drift = random.gauss(0, self.volatility)
        self.mid_price = max(0.05, min(0.95, self.mid_price + drift))
        # Simuler des fills selon la proximité au mid
        self._maybe_fill_orders()

    def place_order(self, side: str, price: float, size: float) -> str:
        """Place un ordre limite dans le carnet simulé.

        Args:
            side: "buy" ou "sell".
            price: prix limite.
            size: quantité.

        Returns:
            L'identifiant de l'ordre placé.
        """
        oid = self._gen_order_id()
        self.open_orders.append(Order(oid, side, price, size, time.time()))
        return oid

    def cancel_all(self) -> None:
        """Annule tous les ordres ouverts (clear du carnet mock)."""
        self.open_orders.clear()

    def _maybe_fill_orders(self) -> None:
        """Remplit probabilistiquement certains ordres ouverts.

        Logique simplifiée:
        - Probabilité de fill = max(0.05, base_prob - distance_au_mid)
        - base_prob ~ 0.3; plus l'ordre est loin du mid, moins il est probable.
        - Mise à jour de l'inventaire et du cash selon le sens de l'ordre.
        """
        filled: List[Order] = []
        for o in self.open_orders:
            # Plus l'ordre est proche du mid, plus il a de chances d'être rempli
            distance = abs(o.price - self.mid_price)
            base_prob = 0.3
            prob = max(0.05, base_prob - distance)  # loin du mid -> prob plus faible
            if random.random() < prob:
                filled.append(o)
        # Appliquer les fills et mettre à jour l'état
        for o in filled:
            if o.side == "buy":
                self.inventory += o.size
                self.cash -= o.size * o.price
            else:
                self.inventory -= o.size
                self.cash += o.size * o.price
            self.open_orders.remove(o)

    def mark_to_market_pnl(self) -> float:
        """Calcule le PnL mark-to-market sur le mid courant.

        Définition: PnL = cash + inventaire * mid.
        """
        # Valeur mark-to-market: cash + inventaire à mid
        return self.cash + self.inventory * self.mid_price

    def status(self) -> dict:
        """Expose un instantané de l'état de l'échange mock.

        Returns:
            dict avec: mid, inventory, cash, pnl, open_orders.
        """
        return {
            "mid": self.mid_price,
            "inventory": self.inventory,
            "cash": self.cash,
            "pnl": self.mark_to_market_pnl(),
            "open_orders": len(self.open_orders),
        }
