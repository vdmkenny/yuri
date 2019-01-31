#!/usr/bin/env python
from configparser import ConfigParser
from pprint import pprint
import sys, time, json

import commands
import common
import config
import gracefulkiller
import rocketapi

def read_messages(channel = None, lastId = None):
  channel_info = config.rocket.channels_info(room_id = channel).json()
  currentId = channel_info['channel']['_updatedAt']
  if currentId != lastId:
    new_message = config.rocket.channels_history(room_id = channel, count=1).json()
    pprint(new_message)
    commands.parse(new_message)
  return currentId

def main():
  killer = gracefulkiller.GracefulKiller()

  # setup
  config.bot = config.read()
  try:
    config.rocket = rocketapi.create_session(config.bot['server_info']['username'],
                                      config.bot['server_info']['password'],
                                      server_url = config.bot['server_info']['server'])
  except:
      sys.exit("failed to connect to rocketchat server!")

  # startup message
  common.send_message("I am up and running!")

  # start listening loop
  bot_running = True
  lastchecked = None

  while bot_running:
    time.sleep(0.100)
    lastchecked = read_messages(channel = config.bot['bot_config']['channel'], lastId=lastchecked)

    if killer.kill_now:
      break

  common.send_message("I'm shutting down NOW!")
  
if __name__ == "__main__":
    main()
