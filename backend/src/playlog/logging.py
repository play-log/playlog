import logging
import sys

from playlog.config import DEBUG


def setup():
    level = logging.NOTSET if DEBUG else logging.WARN

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)
