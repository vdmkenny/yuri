import config
from pprint import pprint

def send_message(msg = None):
    pprint(config.rocket.chat_post_message(msg, channel=config.bot['bot_config']['channel'], alias=config.bot['bot_config']['alias']).json())

