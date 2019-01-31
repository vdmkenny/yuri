import re
from pprint import pprint

import config

def test(message):
  pprint(config.rocket.chat_post_message('This is a reply to the !test command!', channel=config.bot['bot_config']['channel'], alias=config.bot['bot_config']['alias']).json())

def ping(message):
  pprint(config.rocket.chat_post_message('Pong!', channel=config.bot['bot_config']['channel'], alias=config.bot['bot_config']['alias']).json())

def parse(message):
  commands = {'!test': test,
              '!ping': ping,
  }

  is_command = re.match('^\!(.+)', message['messages'][0]['msg'])
  command = message['messages'][0]['msg'].partition(' ')[0]

  if is_command and command in commands:
    commands[command](message)
