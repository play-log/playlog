import logging
import sys

from .config import ENVIRONMENT


def setup_logging():
    debug = ENVIRONMENT == 'development'
    level = logging.NOTSET if debug else logging.WARN

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)
