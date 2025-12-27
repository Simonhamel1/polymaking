"""Client HTTP public Polymarket (base).

Ce client couvre les endpoints publics minimaux (liste des marchés) et
fournit un placeholder pour l'orderbook. Les opérations de trading (CLOB
privé) ne sont PAS implémentées ici et doivent être ajoutées avec gestion
des clés, signatures, latence et erreurs.
"""

import time
from typing import Any, Dict, Optional

import requests


class PolymarketClient:
    """Client minimal pour marchés et placeholder d'orderbook.

    Limites:
    - L'orderbook réel est sur WebSocket (CLOB). Ici, on dérive un mid
      approximatif depuis des champs REST si disponibles.
    - Les méthodes `place_order`/`cancel_order` sont des stubs.
    """

    def __init__(self, api_base: str = "https://api.polymarket.com") -> None:
        self.api_base = api_base.rstrip("/")

    def get_markets(self, active_only: bool = True) -> Dict[str, Any]:
        """Récupère la liste des marchés.

        Args:
            active_only: filtre pour ne garder que les marchés actifs.

        Returns:
            JSON de réponse de l'API.
        """
        url = f"{self.api_base}/markets"
        params = {"active": str(active_only).lower()} if active_only else {}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_orderbook(self, market_id: str) -> Dict[str, Any]:
        """Placeholder d'orderbook basé sur REST.

        Note: Polymarket expose le carnet temps réel via CLOB/WebSocket.
        Cette méthode REST sert uniquement d'exemple et n'est pas
        représentative du flux live.
        """
        url = f"{self.api_base}/markets/{market_id}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Placeholder: dériver mid_price depuis last_trade/price si disponible
        last = data.get("last_trade") or {}
        price = last.get("price") or data.get("price") or 0.5
        return {"mid_price": float(price), "timestamp": time.time(), "raw": data}

    # --- Stubs pour le trading (à implémenter avec CLOB privé) ---
    def place_order(self, market_id: str, side: str, price: float, size: float) -> str:
        """À implémenter: placement d'ordre via CLOB privé."""
        raise NotImplementedError("Trading CLOB non implémenté dans cette base.")

    def cancel_order(self, order_id: str) -> bool:
        """À implémenter: annulation d'ordre via CLOB privé."""
        raise NotImplementedError("Trading CLOB non implémenté dans cette base.")
