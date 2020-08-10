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
        logger.warning('↳ No existing state file, starting with blank state - this should only happen on first launch!')
        save()

def save():
    global mapping

    logger.debug('Saving state...')
    logger.warning(mapping)

    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        with open(MAPPING_PATH, 'w') as file:
            json.dump(mapping, file, indent=2)
            logger.info('State saved')
    except OSError:
        fatal_error(f'↳ Could not save to {MAPPING_PATH}')

def associate_channel(user, channel, channel_type):
    logger.debug(f"Associating user '{user}' with '{channel_type}' channel '{channel.name}'")
    if str(user.id) in mapping:
        mapping[str(user.id)][channel_type] = str(channel.id)
    else:
        mapping[str(user.id)] = {channel_type: str(channel.id)}
    save()

def get_channel_id(user, channel_type):
    try:
        return int(mapping[str(user.id)][channel_type])
    except:
        return None

def owner_of_channel(channel, channel_type):
    for user, channels in mapping.items():
        if str(channel.id) == channels[channel_type]:
            return int(user)

    return None
