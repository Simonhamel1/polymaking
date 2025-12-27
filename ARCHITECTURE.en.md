# Market-Making Bot Architecture (base)

Languages: English (this document) · Français ([ARCHITECTURE.md](ARCHITECTURE.md))

This project provides a modular, extensible base for a market-making bot on Polymarket. It includes a simulated exchange for the demo and interfaces ready for integration with Polymarket's private CLOB API.

## Components

- **Config** (`src/polymarket_maker/config.py`): Loads parameters (mode, spread, quote size, inventory limits, etc.) from environment.
- **Logger** (`src/polymarket_maker/utils/logger.py`): Standard logging configurable via `LOG_LEVEL`.
- **Exchange**:
  - `polymarket_client.py`: Public HTTP client (markets, placeholder order book). Trading methods are stubs.
  - `mock_exchange.py`: Exchange simulator for the demo (mid price, probabilistic fills, inventory/cash/PnL).
- **Strategy**:
  - `base.py`: `Strategy` and `Quote` interfaces.
  - `constant_spread.py`: Constant-spread strategy around the mid.
- **Risk** (`src/polymarket_maker/risk.py`): Simple inventory limit management (quote authorization, size clamp).
- **Runner** (`src/polymarket_maker/runner.py`): Main execution loop; demo mode with the mock exchange.
- **Demo** (`demo/run_demo.py`): Runs a simulated market-making session.

## Execution flow

1. Load config and initialize components (exchange, strategy, risk).
2. Loop:
   - Update mid (mock) and simulate fills.
   - Cancel/replace quotes.
   - Risk check and generate quotes (bid/ask).
   - Place orders.
   - Log state (mid, inventory, cash, PnL, open_orders).
3. Stop after configured duration and log final state.

## Polymarket integration (live)

- **Real-time order book**: Use CLOB WebSocket for receiving the book and mid.
- **Trading**: Implement `place_order` and `cancel_order` in `polymarket_client.py` with authentication (signatures) and error handling.
- **Security**: Store keys in `.env`/vault; limit sizes and leverage; monitor latency and slippage.

## Possible evolutions

- Target inventory and dynamic skew (e.g., bias bid/ask toward underweight side).
- Advanced risk management (drawdown, max orders, cooldowns).
- Backtesting on historical data.
- Persistence (SQLite) for trades and state.

## Reading the code (quick guide)

- **`Quote`**: strategy-side structure describing a limit order proposal with `side` (buy/sell), `price`, `size`.
- **`Strategy`**: interface producing quotes from `mid_price` and `inventory`. Example: `ConstantSpreadStrategy`.
- **`RiskManager`**: applies simple rules (inventory limit) to decide whether to quote and to adjust order size (`clamp_size`).
- **`MockExchange`**: simulated exchange (bounded random mid, probabilistic fills), maintains `inventory`, `cash`, and computes mark-to-market `pnl`.
- **`PolymarketClient`**: public (REST) client for markets; live order book and trading to be implemented via CLOB WebSocket/private.
- **`runner.py`**: demo entry-point; loop that updates mid, cancels/replaces, generates/quotes, and logs the state.

Suggested reading path:
1. `runner.py` (overall loop view).
2. `exchange/mock_exchange.py` (simulated mid and fills).
3. `strategy/constant_spread.py` and `strategy/base.py` (quotes).
4. `risk.py` (inventory limits).
5. `exchange/polymarket_client.py` (REST integration and CLOB TODO).
