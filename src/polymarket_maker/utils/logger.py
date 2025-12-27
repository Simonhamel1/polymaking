"""Utilitaire de logging.

Configure un logger global via `logging.basicConfig` et renvoie un logger
par nom. Le niveau par défaut est contrôlé par la variable d'environnement
`LOG_LEVEL` (INFO par défaut).
"""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Retourne un logger nommé avec niveau/configuration standard.

    Format de log: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`.
    Exemple: `2025-12-27 23:27:30,077 | INFO | runner-demo | ...`
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)
