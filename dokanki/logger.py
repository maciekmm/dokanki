import logging
import sys


def logger(loggername):
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    lout = logging.StreamHandler(sys.stdout)
    lout.setLevel(~logging.ERROR)
    lout.setFormatter(formatter)
    logger.addHandler(lout)

    lerr = logging.StreamHandler(sys.stderr)
    lerr.setLevel(logging.ERROR)
    lerr.setFormatter(formatter)
    logger.addHandler(lerr)
    return logger
