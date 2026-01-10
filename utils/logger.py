import logging
from flask import g, request

def setup_logger():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s request_id=%(request_id)s %(message)s'
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(g, "request_id", "N/A")
        return True

setup_logger().addFilter(RequestIdFilter())