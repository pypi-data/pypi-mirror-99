import logging

logger = logging.getLogger(__name__)


def test_true():
    logger.info("Dummy integration test")
    return True
