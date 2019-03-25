import logging


def logger(loggername):
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('log-data.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
