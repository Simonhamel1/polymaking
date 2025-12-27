class RiskManager:
    def __init__(self, inventory_limit: float) -> None:
        self.limit = float(inventory_limit)

    def allow_new_quotes(self, inventory: float) -> bool:
        return abs(inventory) < self.limit

    def clamp_size(self, desired_size: float, inventory: float) -> float:
        # Réduire la taille si proche de la limite
        remaining = max(0.0, self.limit - abs(inventory))
        return min(desired_size, remaining)
