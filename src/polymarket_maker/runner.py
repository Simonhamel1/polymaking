import argparse
import time

from .config import load_config
from .utils.logger import get_logger
from .exchange.mock_exchange import MockExchange
from .strategy.constant_spread import ConstantSpreadStrategy
from .risk import RiskManager


def run_demo(duration_seconds: int = 30) -> None:
    log = get_logger("runner-demo")
    cfg = load_config()

    exchange = MockExchange(start_mid=0.5, volatility=0.01)
    strat = ConstantSpreadStrategy(spread_bps=cfg.spread_bps, quote_size=cfg.quote_size)
    risk = RiskManager(inventory_limit=cfg.inventory_limit)

    log.info("Démarrage démo market making (mock exchange)")
    t0 = time.time()
    while time.time() - t0 < duration_seconds:
        # Mise à jour du prix simulé et éventuels fills
        exchange.tick()
        mid = exchange.get_mid_price()

        # Cancel/Replace quote style minimal
        exchange.cancel_all()

        if risk.allow_new_quotes(exchange.inventory):
            quotes = strat.generate_quotes(mid, exchange.inventory)
            for q in quotes:
                size = risk.clamp_size(q.size, exchange.inventory)
                if size > 0:
                    exchange.place_order(q.side, q.price, size)
        else:
            pass  # near/in limit, pause quoting

        status = exchange.status()
        log.info(
            f"mid={status['mid']:.4f} inv={status['inventory']:.2f} cash={status['cash']:.2f} pnl={status['pnl']:.2f} open={status['open_orders']}"
        )
        time.sleep(load_config().refresh_seconds)

    log.info("Fin démo. État final: %s", exchange.status())


def main():
    parser = argparse.ArgumentParser(description="Polymarket Maker Runner")
    parser.add_argument("--demo", action="store_true", help="Run mock demo")
    parser.add_argument("--seconds", type=int, default=30, help="Demo duration")
    args = parser.parse_args()

    if args.demo:
        run_demo(args.seconds)
    else:
        raise SystemExit("Seul le mode --demo est implémenté dans cette base.")


if __name__ == "__main__":
    main()
