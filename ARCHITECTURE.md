# Architecture du bot de market making (base)

Ce projet propose une base modulaire et extensible pour un bot de market making sur Polymarket. Il comprend un échange simulé pour la démo et des interfaces prêtes pour l’intégration avec l’API CLOB privée de Polymarket.

## Composants

- **Config** (`src/polymarket_maker/config.py`): Charge les paramètres (mode, spread, taille des quotes, limites d’inventaire, etc.) depuis l’environnement.
- **Logger** (`src/polymarket_maker/utils/logger.py`): Logging standard configurable via `LOG_LEVEL`.
- **Exchange**:
  - `polymarket_client.py`: Client HTTP public (marchés, placeholder orderbook). Les méthodes de trading sont des stubs.
  - `mock_exchange.py`: Simulateur d’échange pour la démo (mid price, fills probabilistes, inventaire/cash/PnL).
- **Strategy**:
  - `base.py`: Interface `Strategy` et `Quote`.
  - `constant_spread.py`: Stratégie de spread constant autour du mid.
- **Risk** (`src/polymarket_maker/risk.py`): Gestion simple des limites d’inventaire (autorisation des quotes, clamp de taille).
- **Runner** (`src/polymarket_maker/runner.py`): Boucle principale d’exécution; mode démo avec le mock exchange.
- **Demo** (`demo/run_demo.py`): Lance une session de market making simulée.

## Flux d’exécution

1. Chargement de la config et initialisation des composants (exchange, strategy, risk).
2. Boucle:
   - Mise à jour du mid price (mock) et simulation des fills.
   - Cancel/replace des quotes.
   - Risk check et génération des quotes (bid/ask).
   - Placement des ordres.
   - Logging de l’état (mid, inventory, cash, PnL, open_orders).
3. Arrêt après la durée configurée et reporting final.

## Intégration Polymarket (live)

- **Orderbook temps réel**: Utiliser le CLOB WebSocket pour recevoir le carnet et le mid.
- **Trading**: Implémenter `place_order` et `cancel_order` dans `polymarket_client.py` avec authentification (signatures) et gestion des erreurs.
- **Sécurité**: Stocker les clés dans `.env`/Azure Key Vault etc.; limiter les tailles et le leverage; surveiller latence et slippage.

## Évolutions possibles

- Inventaire ciblé et skew dynamique (ex: rapprocher le bid/ask côté sous-pondéré).
- Gestion des risques avancée (drawdown, max orders, cooldowns).
- Backtesting sur données historisées.
- Persistance (SQLite) des trades et états.
