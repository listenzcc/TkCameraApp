'''
FileName: SocketUtils.py
Author: Chuncheng
Version: V0.0
Purpose: The Utils Toolbox of Socket
'''

from Logger import logger

coding = 'utf-8'


def decode(content, coding=coding):
    ''' Decode [content] if necessary '''
    t = type(content)
    logger.debug(f'Decoding "{content}", {t}')
    if isinstance(content, type(b'')):
        return content.decode(coding)
    else:
        return content


def encode(content, coding=coding):
    ''' Encode [content] if necessary '''
    t = type(content)
    logger.debug(f'Encoding "{content}", {t}')
    if isinstance(content, type('')):
        return content.encode(coding)
    else:
        return content
