import logging


def get_logger(area):
    logging.basicConfig(filename="logs/request.log", format='%(asctime)s [%(levelname)s]\t %(message)s',
                        datefmt='%H:%M:%S', filemode="w", level=logging.INFO)
    logger = logging.getLogger(area)
    return logger
