import configparser
import sys

#globals
rocket = None
bot = None

def read():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except:
        sys.exit("Can't read config file config.ini!")
    bot = config
    return config
