import config
from pprint import pprint

def send_message(msg = None, img = None):
    pprint(config.rocket.chat_post_message(msg, 
        channel=config.bot['bot_config']['channel'], 
        alias=config.bot['bot_config']['alias'],
        avatar=config.bot['bot_config']['avatar'],
        attachments=[{'image_url': img}]
        ).json())

