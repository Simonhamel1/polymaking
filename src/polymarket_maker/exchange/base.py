from abc import ABC, abstractmethod
from typing import Dict, Any
from ..constants import Side

class Exchange(ABC):
    """Interface abstraite pour interagir avec un marché (réel ou simulé)."""

    @abstractmethod
    def get_mid_price(self) -> float:
        """Retourne le prix mid actuel."""
        pass

    @abstractmethod
    def place_order(self, side: Side, price: float, size: float) -> str:
        """Place un ordre limite.
        
        Returns:
            L'ID de l'ordre placé.
        """
        pass

    @abstractmethod
    def cancel_all(self) -> None:
        """Annule tous les ordres ouverts gérés par ce bot."""
        pass

    @abstractmethod
    def get_portfolio(self) -> Dict[str, float]:
        """Retourne l'état du portefeuille (inventory, cash, pnl)."""
        pass

    def tick(self) -> None:
        """Méthode optionnelle pour avancer la simulation ou poller l'API."""
        pass
