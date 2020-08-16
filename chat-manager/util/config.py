import os
import json
import logging

from .log import fatal_error

logger = logging.getLogger('text-chat-bot')

CONFIG = os.getenv('CONFIG', 'config.json')


def init():
    global config
    logger.info('Loading config...')

    try:
        if CONFIG[0] == '{':
            logger.info('Loading CONFIG as JSON')
            config = json.loads(CONFIG)
        else:
            logger.info('Loading CONFIG as file')
            content = open(CONFIG)
            config = json.load(content)
            print(config)
    except:
        fatal_error(f"↳ Cannot parse '{CONFIG}'")
