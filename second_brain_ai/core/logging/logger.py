import logging
import os
from datetime import datetime


LOG_DIR_BUILD = "logs/ai_build"
LOG_DIR_ERRORS = "logs/errors"
LOG_DIR_METRICS = "logs/metrics"


def _ensure_log_dirs():
    os.makedirs(LOG_DIR_BUILD, exist_ok=True)
    os.makedirs(LOG_DIR_ERRORS, exist_ok=True)
    os.makedirs(LOG_DIR_METRICS, exist_ok=True)


class LoggerFactory:
    """
    Creates standardized loggers for system modules
    """

    @staticmethod
    def create_logger(module_name: str):
        _ensure_log_dirs()

        logger = logging.getLogger(module_name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            log_file = os.path.join(
                LOG_DIR_BUILD,
                f"{module_name}_{datetime.utcnow().date()}.log"
            )

            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger


class ErrorLogger:

    @staticmethod
    def log_error(module_name: str, message: str):
        _ensure_log_dirs()

        log_file = os.path.join(
            LOG_DIR_ERRORS,
            f"errors_{datetime.utcnow().date()}.log"
        )

        with open(log_file, "a") as f:
            f.write(
                f"{datetime.utcnow().isoformat()} | ERROR | {module_name} | {message}\n"
            )


class MetricsLogger:

    @staticmethod
    def log_metric(metric_name: str, value):
        _ensure_log_dirs()

        log_file = os.path.join(
            LOG_DIR_METRICS,
            f"metrics_{datetime.utcnow().date()}.log"
        )

        with open(log_file, "a") as f:
            f.write(
                f"{datetime.utcnow().isoformat()} | {metric_name} | {value}\n"
            )