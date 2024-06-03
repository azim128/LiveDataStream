import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    logger = logging.getLogger("uvicorn.error")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        "logs/app.log", when="midnight", interval=1, backupCount=10
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
