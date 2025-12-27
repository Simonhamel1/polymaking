# Polymarket Market Making Bot (Base)

Langues: Français (ce document) · English ([README.en.md](README.en.md))

Cette base fournit une architecture concrète, une démo exécutable et les briques nécessaires pour développer un bot de market making sur Polymarket.

## Contenu

- [src/polymarket_maker](src/polymarket_maker): Package Python du bot
  - `config.py`: Chargement de configuration via variables d’environnement
  - `utils/logger.py`: Logger configurable
  - `exchange/polymarket_client.py`: Client API public + stubs trading
  - `exchange/mock_exchange.py`: Échange simulé pour la démo
  - `strategy/base.py`: Interface stratégie + structure de quote
  - `strategy/constant_spread.py`: Stratégie à spread constant
  - `risk.py`: Gestion simple des limites d’inventaire
  - `runner.py`: Boucle principale; mode `--demo`
- [demo/run_demo.py](demo/run_demo.py): Lance la démo
- [ARCHITECTURE.md](ARCHITECTURE.md): Détails de l’architecture
- [requirements.txt](requirements.txt): Dépendances Python

## Prérequis

- Python 3.10+ (Windows supporté)

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer la démo

Deux options équivalentes:

```bash
# Via le runner
python src/polymarket_maker/runner.py --demo --seconds 30

# Via le script démo
python demo/run_demo.py
```

Vous verrez dans la console les logs: mid, inventory, cash, PnL, et nombre d’ordres ouverts. La démo utilise un échange simulé (mock) et une stratégie à spread constant.

## Configuration (facultatif)

Vous pouvez créer un fichier `.env` pour surcharger les valeurs par défaut:

```
PM_MODE=demo
PM_SPREAD_BPS=50
PM_QUOTE_SIZE=100
PM_INVENTORY_LIMIT=1000
PM_REFRESH_SECONDS=1
PM_USE_MOCK=true
PM_API_BASE=https://api.polymarket.com
LOG_LEVEL=INFO
```

## Passage en mode live (à implémenter)

- Implémenter la connexion au CLOB (WebSocket) pour l’orderbook.
- Implémenter `place_order`/`cancel_order` dans `exchange/polymarket_client.py` avec l’auth et les signatures.
- Ajouter une gestion des erreurs, des timeouts et des retours d’état.
- Sécuriser les secrets via `.env` (ou coffre-fort) et limiter les tailles d’ordres.

Pour l’architecture détaillée et les pistes d’évolution, consultez [ARCHITECTURE.md](ARCHITECTURE.md).

## Licence
MIT License. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
