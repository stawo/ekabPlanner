import logging

def custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.FileHandler(name+".log", mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    #~ logger.setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
