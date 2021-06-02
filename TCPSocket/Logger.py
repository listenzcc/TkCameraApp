'''
FileName: Logger.py
Author: Chuncheng
Version: V0.0
Purpose: Establish the Logger for the Python Scripts
'''


import logging

# Make Logger


def mk_logger(name, level, fmt):
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


kwargs = dict(
    name='CameraApp',
    level=logging.DEBUG,
    fmt='%(asctime)s - %(levelname)s - %(message)s - (%(filename)s %(lineno)d)'
)

logger = mk_logger(**kwargs)
logger.info('Package Initialized')
