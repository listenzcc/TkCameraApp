'''
FileName: __init__.py
Author: Chuncheng
Version: V0.0
Purpose: Init the Package
'''


import logging


# ------------------------------------------------------------------------------
# Logger


# Make Logger

def mk_logger(name, level, fmt):
    '''
    Method:mk_logger

    Make Logger

    Args:
    - @name, level, fmt

    Outputs:
    - The logger object

    '''

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


# ------------------------------------------------------------------------------
# Utils

coding = 'utf-8'


def decode(content, coding=coding):
    ''' Decode [content] if necessary '''
    t = type(content)
    logger.debug(f'Decoding "content", {t}')
    if isinstance(content, type(b'')):
        return content.decode(coding)
    else:
        return content


def encode(content, coding=coding):
    ''' Encode [content] if necessary '''
    t = type(content)
    logger.debug(f'Encoding "content", {t}')
    if isinstance(content, type('')):
        return content.encode(coding)
    else:
        return content
