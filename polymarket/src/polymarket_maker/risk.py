"""Gestion des risques minimaliste pour la démo.

Ce module implémente des contrôles simples basés sur la limite d'inventaire:
- Autoriser/suspendre le quoting selon la position actuelle.
- Réduire la taille des ordres lorsque la limite est proche.
"""


class RiskManager:
    """Contrôles basés sur une limite d'inventaire absolue."""

    def __init__(self, inventory_limit: float) -> None:
        self.limit = float(inventory_limit)

    def allow_new_quotes(self, inventory: float) -> bool:
        """Retourne True si on peut encore coter sans dépasser la limite."""
        return abs(inventory) < self.limit

    def clamp_size(self, desired_size: float, inventory: float) -> float:
        """Réduit la taille demandée si proche de la limite.

        Calcul: remaining = max(0, limite - |inventaire|), puis `min`.
        """
        # Réduire la taille si proche de la limite
        remaining = max(0.0, self.limit - abs(inventory))
        return min(desired_size, remaining)
