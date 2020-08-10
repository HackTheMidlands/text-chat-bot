import os
import sys
import logging
import datetime

LOG_PATH = 'logs'
CONSOLE_LEVEL = logging.DEBUG
FILE_LEVEL = logging.INFO

def init():
    os.makedirs(LOG_PATH, exist_ok=True)

    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'FATAL')
    logger = logging.getLogger('text-chat-bot')
    logger.setLevel(logging.DEBUG)

    console_format = logging.Formatter('%(levelname)5s %(module)6s: %(message)s')
    file_format = logging.Formatter('%(levelname)5s %(module)6s: %(message)s')

    file_handler = logging.FileHandler(filename=f'{LOG_PATH}/{datetime.datetime.utcnow()}.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(file_format)
    file_handler.setLevel(FILE_LEVEL)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    console_handler.setLevel(CONSOLE_LEVEL)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def fatal_error(*args, **kwargs):
    logger = logging.getLogger('text-chat-bot')
    logger.critical(*args, **kwargs)
    sys.exit(1)
