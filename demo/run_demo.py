"""Demo runner for the Polymarket market-making bot.

This script runs the mock demo for a short duration. Use PowerShell and set
PYTHONPATH to the src folder if running from the repo root on Windows.
"""

from polymarket_maker.runner import run_demo


if __name__ == "__main__":
    # Default: 30 seconds; adjust if needed
    run_demo(30)
