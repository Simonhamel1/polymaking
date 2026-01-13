# Polymarket Market Maker Bot

Ce projet fournit une base modulaire, robuste et typée pour développer des bots de trading (Market Making) sur Polymarket. Il est conçu pour être facilement extensible, testable (via un mode Mock) et prêt pour la production.

## 🚀 Fonctionnalités Clés

- **Architecture Modulaire** : Séparation claire entre le moteur (`Bot`), l'échange (`Exchange`), la stratégie (`Strategy`) et le risque (`Risk`).
- **Typage Strict** : Utilisation de `dataclasses` et `Enum` (ex: `Side.BUY`) pour réduire les bugs.
- **Mode Simulation (Mock)** : Un échange simulé inclus (`MockExchange`) avec carnet d'ordres, fills probabilistes et suivi du PnL en temps réel.
- **Gestion des Risques** : Module de base pour limiter l'inventaire et la taille des ordres.
- **Extensible** : Interface `Exchange` abstraite prête pour implémenter l'API réelle de Polymarket (CLOB).

## 📂 Structure du Projet

```text
src/polymarket_maker/
├── bot.py              # Moteur principal (boucle d'exécution, orchestration)
├── config.py           # Chargement de la configuration (env vars)
├── constants.py        # Définitions des types (Side, etc.)
├── runner.py           # Point d'entrée CLI
├── exchange/
│   ├── base.py         # Interface abstraite Exchange (le contrat à respecter)
│   └── mock_exchange.py # Simulation locale pour dev et tests
├── strategy/
│   ├── base.py         # Interface abstraite Strategy
│   └── constant_spread.py # Exemple : Stratégie de spread fixe
└── utils/
    └── logger.py       # Configuration des logs
```

## 🛠 Installation

1. **Prérequis** : Python 3.9+
2. **Installation des dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Démarrage Rapide (Démo)

Lancez le bot en mode simulation pour voir la stratégie agir sur un marché fictif :

```bash
python demo/run_demo.py
```

Vous verrez les logs du bot affichant le prix Mid, l'inventaire, le PnL et les ordres placés.

## ⚙️ Configuration

Le bot se configure via des variables d'environnement (fichier `.env` recommandé) ou via les arguments par défaut dans `config.py`.

| Variable | Défaut | Description |
| :--- | :--- | :--- |
| `PM_MODE` | `demo` | Mode de fonctionnement. |
| `PM_SPREAD_BPS` | `50` | Spread en points de base (50 bps = 0.5%). |
| `PM_QUOTE_SIZE` | `100` | Taille des ordres limites. |
| `PM_INVENTORY_LIMIT`| `1000` | Position maximale autorisée (Long ou Short). |
| `PM_REFRESH_SECONDS`| `1.0` | Temps d'attente entre deux cycles. |
| `PM_USE_MOCK` | `true` | Si `true`, utilise le `MockExchange`. |

## 🏗 Guide de Développement

### 1. Créer une nouvelle stratégie
Héritez de `Strategy` dans `src/polymarket_maker/strategy/base.py` :

```python
from .base import Strategy, Quote
from ..constants import Side

class MaStrategie(Strategy):
    def generate_quotes(self, mid_price, inventory):
        # Votre logique ici
        return [Quote(Side.BUY, mid_price - 0.05, 10)]
```

### 2. Connecter l'API Réelle (Polymarket CLOB)
Créez une classe `PolymarketExchange` dans `src/polymarket_maker/exchange/` qui hérite de `Exchange`. Vous devrez implémenter :
- `get_mid_price()`
- `place_order()`
- `cancel_all()`
- `get_portfolio()`

Une fois implémentée, mettez à jour `src/polymarket_maker/runner.py` pour utiliser cette classe quand `use_mock` est `False`.

## 🛡 Gestion des Risques
Le `RiskManager` actuel (`src/polymarket_maker/risk.py`) implémente :
- **Limite d'inventaire** : Arrête de quoter si l'exposition est trop forte.
- **Clamping** : Réduit la taille des nouveaux ordres pour ne pas dépasser la limite exacte.

## 📝 Licence
Ce projet est une base open-source pour l'apprentissage et le développement de bots de trading.