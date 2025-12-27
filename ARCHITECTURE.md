# Architecture du bot de market making (base)

Langues: Français (ce document) · English ([ARCHITECTURE.en.md](ARCHITECTURE.en.md))

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

## Lecture du code (guide rapide)

- **`Quote`**: structure (côté stratégie) décrivant une proposition d’ordre
  avec `side` (buy/sell), `price`, `size`.
- **`Strategy`**: interface qui produit des quotes à partir du `mid_price`
  et de l’`inventory`. Implémentation exemple: `ConstantSpreadStrategy`.
- **`RiskManager`**: applique des règles simples (limite d’inventaire) pour
  décider si on cote et pour ajuster la taille des ordres (`clamp_size`).
- **`MockExchange`**: échange simulé (mid aléatoire borné, fills
  probabilistes), maintient `inventory`, `cash`, et calcule le `pnl` M2M.
- **`PolymarketClient`**: client public (REST) pour marchés; orderbook live
  et trading à implémenter via CLOB WebSocket/privé.
- **`runner.py`**: point d’entrée de la démo; boucle qui met à jour le mid,
  annule/remplace, génère/cote des quotes, et log l’état.

Chemin de lecture recommandé:
1. `runner.py` (vision d’ensemble de la boucle).
2. `exchange/mock_exchange.py` (mid et fills simulés).
3. `strategy/constant_spread.py` et `strategy/base.py` (quotes).
4. `risk.py` (limites d’inventaire).
5. `exchange/polymarket_client.py` (intégration REST et TODO CLOB).

## Reading the code (quick guide)

- **`Quote`**: strategy-side structure describing a limit order proposal with
  `side` (buy/sell), `price`, `size`.
- **`Strategy`**: interface producing quotes from `mid_price` and `inventory`.
  Example implementation: `ConstantSpreadStrategy`.
- **`RiskManager`**: applies simple rules (inventory limit) to decide whether
  to quote and to adjust order size (`clamp_size`).
- **`MockExchange`**: simulated exchange (bounded random mid, probabilistic
  fills), maintains `inventory`, `cash`, and computes mark-to-market `pnl`.
- **`PolymarketClient`**: public (REST) client for markets; live order book
  and trading to be implemented via CLOB WebSocket/private.
- **`runner.py`**: demo entry-point; loop that updates mid, cancels/replaces,
  generates/quotes, and logs the state.

Suggested reading path:
1. `runner.py` (overall loop view).
2. `exchange/mock_exchange.py` (simulated mid and fills).
3. `strategy/constant_spread.py` and `strategy/base.py` (quotes).
4. `risk.py` (inventory limits).
5. `exchange/polymarket_client.py` (REST integration and CLOB TODO).
