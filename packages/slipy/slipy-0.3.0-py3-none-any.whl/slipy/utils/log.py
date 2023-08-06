# -*- coding: utf-8 -*-
import logging
import os

# read environment
debug = bool(os.environ.get("DEBUG", False))

module_name = __name__.split(".")[0]
logger = logging.getLogger(module_name)


def setup(log_level=logging.INFO, log_to_stdout=True, log_to_file=None):
    """
    Init logging
    """
    logger.setLevel(log_level)
    # add rich logger
    if log_to_stdout:
        from rich.logging import RichHandler  # pylint: disable=import-outside-toplevel

        rh = RichHandler(log_level)
        rh.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(rh)
    # add file logger
    if log_to_file is not None:
        fh = logging.FileHandler(log_to_file)
        logger.addHandler(fh)
