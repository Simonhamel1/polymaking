"""Runner principal de l'application.

Point d'entrée pour lancer le bot. Charge la configuration, initialise
les composants (Exchange, Strategy, Risk) et lance le moteur (Bot).
"""

import argparse
import sys

from .config import load_config
from .exchange.mock_exchange import MockExchange
from .strategy.constant_spread import ConstantSpreadStrategy
from .risk import RiskManager
from .bot import MarketMakerBot
from .utils.logger import get_logger

def main():
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(description="Polymarket Maker Bot")
    parser.add_argument("--demo", action="store_true", help="Force mock demo mode")
    parser.add_argument("--seconds", type=int, default=30, help="Demo duration in seconds")
    args = parser.parse_args()

    # Chargement de la config
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Erreur de chargement config: {e}")
        sys.exit(1)

    log = get_logger("main")

    # 1. Initialisation de l'Exchange
    # Priorité au flag --demo, sinon config.use_mock
    if args.demo or cfg.use_mock:
        log.info("Mode Mock activé.")
        exchange = MockExchange(start_mid=0.5)
    else:
        # TODO: Implémenter l'adaptateur pour le vrai client Polymarket
        log.error("Le mode Live (Real Exchange) n'est pas encore implémenté.")
        sys.exit(1)

    # 2. Initialisation Stratégie & Risque
    strat = ConstantSpreadStrategy(spread_bps=cfg.spread_bps, quote_size=cfg.quote_size)
    risk = RiskManager(inventory_limit=cfg.inventory_limit)

    # 3. Création et lancement du Bot
    bot = MarketMakerBot(exchange, strat, risk, cfg)
    
    # Si --demo ou use_mock est activé, on peut vouloir une durée limite par défaut
    duration = args.seconds if args.demo else None
    
    bot.run(duration=duration)


if __name__ == "__main__":
    main()