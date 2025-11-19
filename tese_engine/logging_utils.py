"""
TESE V9 - Logging Utilities

Pequena camada de conveniência em cima do logging padrão do Python,
para termos logs consistentes em:

    /data/logs/tese.log

Formato:
    2025-11-19 10:12:30 [INFO] analysis_runner: mensagem...
"""

from __future__ import annotations

import logging
from pathlib import Path


_LOGGER_CACHE = {}


def _get_logs_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    logs_dir = data_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / "tese.log"


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado que escreve em data/logs/tese.log.
    Usa cache interno para não adicionar handlers duplicados.
    """
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita handlers duplicados se get_logger for chamado mais de uma vez
    if not logger.handlers:
        log_path = _get_logs_path()
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        fh.setFormatter(formatter)

        logger.addHandler(fh)

    _LOGGER_CACHE[name] = logger
    return logger
