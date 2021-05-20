'''
File: __init__.py
Author: Chuncheng
Version: 0.0
Purpose: Ensure the folder is a Package
'''

# Imports
import os
import logging

# Package Info
PackageInfo = dict(
    packageName='CameraApp',
    rootDir=os.path.join(os.path.dirname(__file__)),
    dataDir=os.path.join(os.environ['SYNC'], 'CameraAppData')
)

if not os.path.isdir(PackageInfo['dataDir']):
    os.mkdir(PackageInfo['dataDir'])


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
