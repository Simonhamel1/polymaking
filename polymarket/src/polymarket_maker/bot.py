import time
from typing import Optional

from .config import AppConfig
from .exchange.base import Exchange
from .strategy.base import Strategy
from .risk import RiskManager
from .utils.logger import get_logger

class MarketMakerBot:
    """Moteur principal du market making.

    Orchestre les interactions entre l'Exchange, la Strategy et le RiskManager.
    """

    def __init__(
        self,
        exchange: Exchange,
        strategy: Strategy,
        risk: RiskManager,
        config: AppConfig
    ):
        self.exchange = exchange
        self.strategy = strategy
        self.risk = risk
        self.config = config
        self.logger = get_logger("bot")
        self.running = False

    def run(self, duration: Optional[int] = None) -> None:
        """Lance la boucle principale de market making.

        Args:
            duration: Durée optionnelle en secondes (pour les démos/tests).
        """
        self.logger.info(f"Démarrage du Bot (Spread: {self.config.spread_bps}bps, Size: {self.config.quote_size})")
        self.running = True
        start_time = time.time()

        try:
            while self.running:
                self.step()

                # Gestion de la durée (mode démo)
                if duration and (time.time() - start_time > duration):
                    self.logger.info("Durée maximale atteinte. Arrêt.")
                    break
                
                # Attente avant le prochain cycle
                time.sleep(self.config.refresh_seconds)

        except KeyboardInterrupt:
            self.logger.info("Arrêt manuel détecté (Ctrl+C).")
        except Exception as e:
            self.logger.error(f"Erreur critique dans la boucle du bot: {e}", exc_info=True)
            raise
        finally:
            self.shutdown()

    def step(self) -> None:
        """Exécute un cycle unique de trading."""
        # 1. Mise à jour de l'état du marché
        self.exchange.tick()
        mid = self.exchange.get_mid_price()
        portfolio = self.exchange.get_portfolio()
        inventory = portfolio.get("inventory", 0.0)

        # 2. Annulation des ordres existants (stratégie simple: cancel-all)
        self.exchange.cancel_all()

        # 3. Vérification du risque et génération de quotes
        if self.risk.allow_new_quotes(inventory):
            quotes = self.strategy.generate_quotes(mid, inventory)
            
            quotes_placed = 0
            for q in quotes:
                # Clamp de la taille selon le risque
                size = self.risk.clamp_size(q.size, inventory)
                if size > 0:
                    self.exchange.place_order(q.side, q.price, size)
                    quotes_placed += 1
            
            if quotes_placed == 0:
                self.logger.debug("Aucune quote placée (inventaire plein ou spread impossible).")
        else:
            self.logger.warning("Quoting suspendu: limite d'inventaire atteinte.")

        # 4. Logging de suivi
        self._log_status(mid, portfolio)

    def _log_status(self, mid: float, portfolio: dict) -> None:
        inv = portfolio.get("inventory", 0.0)
        pnl = portfolio.get("pnl", 0.0)
        cash = portfolio.get("cash", 0.0)
        self.logger.info(f"Mid: {mid:.4f} | Inv: {inv:.2f} | PnL: {pnl:.2f} | Cash: {cash:.2f}")

    def shutdown(self) -> None:
        """Procédure d'arrêt propre."""
        self.logger.info("Arrêt du bot en cours...")
        try:
            self.exchange.cancel_all()
            self.logger.info("Ordres annulés.")
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage final: {e}")
        self.running = False
