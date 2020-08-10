import sys
import json
import logging

from .log import fatal_error

logger = logging.getLogger('text-chat-bot')

CONFIG_PATH = 'config.json'

def init():
    global config
    logger.info('Loading config...')

    try:
        with open(CONFIG_PATH) as file:
            try:
                config = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal_error(f"↳ Cannot parse '{CONFIG_PATH}'")

    except OSError:
        fatal_error(f"↳ Cannot open '{CONFIG_PATH}'")
