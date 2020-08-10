import logging

from .util import log
log.init()

from .util import config
config.init()

from .util import data
data.init()

from .bot import bot

logger = logging.getLogger('text-chat-bot')
VERSION = '0.1.0-beta.1'

def init():
	logger.info(f'Starting text-chat-bot v{VERSION}')
	bot.start()
