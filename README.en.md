# Polymarket Market Making Bot (Base)

Languages: English (this document) · Français ([README.fr.md](README.fr.md))

This base provides a concrete architecture, a runnable demo, and the building blocks to develop a market-making bot on Polymarket.

## Contents

- [src/polymarket_maker](src/polymarket_maker): Python package for the bot
  - `config.py`: Configuration via environment variables
  - `utils/logger.py`: Configurable logger
  - `exchange/polymarket_client.py`: Public API client + trading stubs
  - `exchange/mock_exchange.py`: Simulated exchange for the demo
  - `strategy/base.py`: Strategy interface + quote structure
  - `strategy/constant_spread.py`: Constant spread strategy
  - `risk.py`: Simple inventory limit management
  - `runner.py`: Main loop; `--demo` mode
- [demo/run_demo.py](demo/run_demo.py): Runs the demo
- [ARCHITECTURE.md](ARCHITECTURE.md): Architecture details
- [requirements.txt](requirements.txt): Python dependencies

## Prerequisites

- Python 3.10+ (Windows supported)

## Installation

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run the demo

Two equivalent options:

```bash
# Via the runner
python src/polymarket_maker/runner.py --demo --seconds 30

# Via the demo script
python demo/run_demo.py
```

You will see logs in the console: mid, inventory, cash, PnL, and number of open orders. The demo uses a simulated exchange (mock) and a constant-spread strategy.

## Configuration (optional)

You can create a `.env` file to override defaults:

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

## Going live (to implement)

- Implement CLOB (WebSocket) connection for the order book.
- Implement `place_order`/`cancel_order` in `exchange/polymarket_client.py` with auth and signatures.
- Add robust error handling, timeouts, and status returns.
- Secure secrets via `.env` (or vault) and limit order sizes.

For detailed architecture and evolution ideas, see [ARCHITECTURE.md](ARCHITECTURE.md).

## License
MIT License. See [LICENSE](LICENSE) for details.
