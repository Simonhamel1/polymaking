# Démo du bot de market making

Ce document montre comment exécuter la démo et à quoi ressemble la sortie.

## Prérequis
- Python 3.10+
- Environnement virtuel (recommandé)

## Installation rapide
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer la démo
Deux façons équivalentes:
```bash
# Option 1 : via le runner en mode module
$env:PYTHONPATH="C:/Users/X515/Documents/GitHub/polymaking/src"
C:/Users/X515/Documents/GitHub/polymaking/.venv/Scripts/python.exe -m polymarket_maker.runner --demo --seconds 30

# Option 2 : via le script démo
C:/Users/X515/Documents/GitHub/polymaking/.venv/Scripts/python.exe demo/run_demo.py
```

## Sortie attendue (exemple)
Pendant l'exécution, vous verrez des logs indiquant le mid, l'inventaire, le cash, le PnL et le nombre d'ordres ouverts.

```
2025-12-27 23:27:30,077 | INFO | runner-demo | Démarrage démo market making (mock exchange)
2025-12-27 23:27:30,078 | INFO | runner-demo | mid=0.5039 inv=0.00 cash=0.00 pnl=0.00 open=2
2025-12-27 23:27:31,078 | INFO | runner-demo | mid=0.4964 inv=0.00 cash=0.00 pnl=0.00 open=2
2025-12-27 23:27:34,082 | INFO | runner-demo | mid=0.5095 inv=-100.00 cash=50.66 pnl=-0.29 open=2
2025-12-27 23:27:36,084 | INFO | runner-demo | mid=0.5063 inv=100.00 cash=-49.92 pnl=0.71 open=2
2025-12-27 23:27:39,087 | INFO | runner-demo | mid=0.5104 inv=0.00 cash=-0.18 pnl=-0.18 open=2
2025-12-27 23:27:40,088 | INFO | runner-demo | Fin démo. État final: { 'mid': 0.5103, 'inventory': 0.0, 'cash': -0.18, 'pnl': -0.18, 'open_orders': 2 }
```

## Paramétrage (facultatif)
Vous pouvez créer un fichier `.env` à la racine pour ajuster la configuration:
```
PM_MODE=demo
PM_SPREAD_BPS=50
PM_QUOTE_SIZE=100
PM_INVENTORY_LIMIT=1000
PM_REFRESH_SECONDS=1
PM_USE_MOCK=true
LOG_LEVEL=INFO
```

## Dépannage rapide
- Erreur d'import relatif: lancez en mode module avec `$env:PYTHONPATH` comme indiqué ci-dessus.
- Pas de logs: vérifiez que `LOG_LEVEL=INFO`.
- PnL inattendu: la démo est simulée (mock), les fills sont probabilistes.
