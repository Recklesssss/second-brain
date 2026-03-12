from core.logging.logger import get_logger, configure_logging


def test_logger_creation():

    configure_logging()

    logger = get_logger("test_module")

    assert logger is not None


def test_logger_write():

    configure_logging()

    logger = get_logger("test")

    logger.info("test message")

    assert True