# Market-Making Bot Demo

Languages: English (this document) · Français ([README.fr.md](README.fr.md))

This document shows how to run the demo and what the output looks like.

## Prerequisites
- Python 3.10+
- Virtual environment (recommended)

## Quick install
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run the demo
Two equivalent ways:
```powershell
# Option 1: via the runner as a module
$env:PYTHONPATH="C:/Users/X515/Documents/GitHub/polymaking/src"
C:/Users/X515/Documents/GitHub/polymaking/.venv/Scripts/python.exe -m polymarket_maker.runner --demo --seconds 30

# Option 2: via the demo script
C:/Users/X515/Documents/GitHub/polymaking/.venv/Scripts/python.exe demo/run_demo.py
```

## Expected output (example)
During execution you will see logs indicating the mid, inventory, cash, PnL, and number of open orders.

```
2025-12-27 23:27:30,077 | INFO | runner-demo | Starting market-making demo (mock exchange)
2025-12-27 23:27:30,078 | INFO | runner-demo | mid=0.5039 inv=0.00 cash=0.00 pnl=0.00 open=2
2025-12-27 23:27:31,078 | INFO | runner-demo | mid=0.4964 inv=0.00 cash=0.00 pnl=0.00 open=2
2025-12-27 23:27:34,082 | INFO | runner-demo | mid=0.5095 inv=-100.00 cash=50.66 pnl=-0.29 open=2
2025-12-27 23:27:36,084 | INFO | runner-demo | mid=0.5063 inv=100.00 cash=-49.92 pnl=0.71 open=2
2025-12-27 23:27:39,087 | INFO | runner-demo | mid=0.5104 inv=0.00 cash=-0.18 pnl=-0.18 open=2
2025-12-27 23:27:40,088 | INFO | runner-demo | Demo end. Final state: { 'mid': 0.5103, 'inventory': 0.0, 'cash': -0.18, 'pnl': -0.18, 'open_orders': 2 }
```

## Configuration (optional)
You can create a `.env` file at the repo root to adjust configuration:
```
PM_MODE=demo
PM_SPREAD_BPS=50
PM_QUOTE_SIZE=100
PM_INVENTORY_LIMIT=1000
PM_REFRESH_SECONDS=1
PM_USE_MOCK=true
LOG_LEVEL=INFO
```

## Quick troubleshooting
- Import error (relative paths): run in module mode with `$env:PYTHONPATH` as shown above.
- No logs: ensure `LOG_LEVEL=INFO`.
- Unexpected PnL: the demo is simulated (mock); fills are probabilistic.
