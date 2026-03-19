import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from second_brain_ai.config.settings import get_settings


class JsonFormatter(logging.Formatter):
    """
    JSON log formatter aligned with logging_schema.
    """

    def format(self, record: logging.LogRecord) -> str:

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "event": getattr(record, "event", "log"),
            "message": record.getMessage(),
        }

        return json.dumps(log_record)


def _ensure_log_directories(root: Path):

    (root / "logs").mkdir(exist_ok=True)
    (root / "logs" / "ai_build").mkdir(parents=True, exist_ok=True)
    (root / "logs" / "errors").mkdir(parents=True, exist_ok=True)
    (root / "logs" / "metrics").mkdir(parents=True, exist_ok=True)


def configure_logging():

    settings = get_settings()

    root = settings.project_root
    _ensure_log_directories(root)

    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    formatter = JsonFormatter()

    ai_build_handler = logging.FileHandler(root / "logs" / "ai_build" / "build.log")
    ai_build_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(root / "logs" / "errors" / "errors.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(ai_build_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieve configured logger.
    """

    return logging.getLogger(name)