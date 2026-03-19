import logging
import os
from pathlib import Path
from datetime import datetime

def setup_observability_loggers():
    base_dir = Path(__file__).resolve().parent.parent / "logs"
    
    build_dir = base_dir / "ai_build"
    error_dir = base_dir / "errors"
    metrics_dir = base_dir / "metrics"

    for d in [build_dir, error_dir, metrics_dir]:
        d.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Build Logger
    build_logger = logging.getLogger("ai_build")
    build_logger.setLevel(logging.INFO)
    build_handler = logging.FileHandler(build_dir / f"build_{timestamp}.log")
    build_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    if not build_logger.handlers:
        build_logger.addHandler(build_handler)

    # Error Logger
    error_logger = logging.getLogger("errors")
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(error_dir / f"error_{timestamp}.log")
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
    if not error_logger.handlers:
        error_logger.addHandler(error_handler)

    # Metrics Logger
    metrics_logger = logging.getLogger("metrics")
    metrics_logger.setLevel(logging.INFO)
    metrics_handler = logging.FileHandler(metrics_dir / f"metrics_{timestamp}.log")
    metrics_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    if not metrics_logger.handlers:
        metrics_logger.addHandler(metrics_handler)

    return build_logger, error_logger, metrics_logger

build_log, error_log, metrics_log = setup_observability_loggers()
