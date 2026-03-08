import os
from core.logging.logger import LoggerFactory, ErrorLogger, MetricsLogger


def test_logger_creation():
    logger = LoggerFactory.create_logger("test_module")
    logger.info("test message")

    assert logger.name == "test_module"


def test_error_logging():
    ErrorLogger.log_error("test_module", "sample error")

    assert os.path.exists("logs/errors")


def test_metrics_logging():
    MetricsLogger.log_metric("test_metric", 1)

    assert os.path.exists("logs/metrics")