import logging


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=handler)

    return logger