import string
import random
import logging

logger = logging.getLogger('text-chat-bot')

PREFIX = 'channel-'
RANDOM_CHAR_COUNT = 12
RANDOM_CHARS = '0123456789abcdef'

def gen_name():
    random_part = ''.join(random.choice(RANDOM_CHARS) for _ in range(RANDOM_CHAR_COUNT))

    return f'{PREFIX}{random_part}'
