import logging


def get_logger():
    logger = logging.getLogger(__name__)
    level = "debug"
    if level == "debug":
        logger.setLevel(level=logging.DEBUG)
    elif level == "info":
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARN)
    console = logging.StreamHandler()
    format_str = "%(asctime)s\t%(levelname)s -- %(filename)s:%(lineno)s -- %(message)s"
    console.setFormatter(logging.Formatter(format_str))
    logger.addHandler(console)

    return logger
