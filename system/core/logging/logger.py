import logging
import json
import sys
from datetime import datetime
from core.config.settings import settings


class JSONFormatter(logging.Formatter):
    def format(self, record):

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging():

    handler = logging.StreamHandler(sys.stdout)

    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    root_logger.addHandler(handler)


setup_logging()