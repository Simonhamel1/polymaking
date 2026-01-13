"""Demo runner for the Polymarket market-making bot.

This script demonstrates how to instantiate the MarketMakerBot programmatically.
"""

import sys
import os

# Ajout de 'src' au PYTHONPATH pour trouver le package polymarket_maker
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from polymarket_maker.config import load_config
from polymarket_maker.exchange.mock_exchange import MockExchange
from polymarket_maker.strategy.constant_spread import ConstantSpreadStrategy
from polymarket_maker.risk import RiskManager
from polymarket_maker.bot import MarketMakerBot

def main():
    print(">>> Initialisation de la démo (Mode Programmatique)")
    cfg = load_config()
    
    # 1. On force l'utilisation du MockExchange pour cette démo
    exchange = MockExchange(start_mid=0.5, volatility=0.02)
    
    # 2. Stratégie et Risque
    strat = ConstantSpreadStrategy(spread_bps=50.0, quote_size=10.0)
    risk = RiskManager(inventory_limit=500.0)
    
    # 3. Création du Bot
    bot = MarketMakerBot(exchange, strat, risk, cfg)
    
    print(">>> Lancement du bot pour 5 secondes...")
    bot.run(duration=5)
    print(">>> Démo terminée avec succès.")

if __name__ == "__main__":
    main()