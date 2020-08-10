import os
import sys
import json
import logging

from .log import fatal_error

logger = logging.getLogger('text-chat-bot')

DATA_PATH = 'data'
MAPPING_PATH = f'{DATA_PATH}/mapping.json'

def init():
    global mapping

    logger.info('Loading state...')
    try:
        with open(MAPPING_PATH, 'r') as file:
            try:
                mapping = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal_error(f'↳ Cannot parse {MAPPING_PATH}')

    except OSError:
        mapping = {}
        logger.warn('↳ No existing state file, starting with blank state - this should only happen on first launch!')
        save()

def save():
    global mapping

    logger.debug('Saving state...')

    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        with open(MAPPING_PATH, 'w') as file:
            json.dump(mapping, file, indent=2)
            logger.info('State saved')
    except OSError:
        fatal_error(f'↳ Could not save to {MAPPING_PATH}')

def associate_channel(user, channel):
    logger.debug(f'Associating user \'{user}\' with channel \'{channel.name}\'')
    mapping[str(user.id)] = str(channel.id)
    save()

def get_channel_id(user):
    try:
        return int(mapping[str(user.id)])
    except:
        return None

def owner_of_channel(channel):
    for user, channel_id in mapping.items():
        if str(channel.id) == channel_id:
            return int(user)

    return None
