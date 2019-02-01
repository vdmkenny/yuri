from giphy_client.rest import ApiException
from pprint import pprint
import giphy_client
import re, sys
import time
import requests

import config
import common

sys.path.append('duckduckgo')
import DuckDuckGo

commands = None


def test(message, param):
  common.send_message('This is a reply to the !test command!')

def ping(message, param):
  common.send_message('Pong!')

def ddg(message, param):
  q = DuckDuckGo.search(param)
  if q.answer.answer:
    common.send_message("*" + param  + "*:\n" + q.answer.answer)
  elif q.definition.definition:
    common.send_message("*" + param  + "*:\n" + q.definition.definition + "\n" + q.definition.definition_url)
  elif q.abstract.abstract:
    common.send_message("*" + q.abstract.heading + "*:\n" + q.abstract.abstract_text + "\n" + q.abstract.abstract_url, q.abstract.image)
  elif q.results:
    common.send_message("*" + param  + "*:\n" + q.results[0].text + "\n" + q.results[0].first_url)
  elif q.related_topics:
    common.send_message("*" + param  + "*:\n" + q.related_topics[0].text + "\n" + q.related_topics[0].first_url)
  elif q.redirect:
    common.send_message("*" + param  + "*:\n" + q.redirect)
  else:
    common.send_message("I couldn't find anything for _" + param + "_!")

def gif(message, param):
  api_instance = giphy_client.DefaultApi()
  try:
    api_key = config.bot['giphy']['api_key'] 
    rating = config.bot['giphy']['rating'] # str | Filters results by specified rating. (optional)
    lang = config.bot['giphy']['lang'] # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
  except:
    common.send_message("Failed to get giphy configurationn")

  q = param # str | Search query term or prhase.
  limit = 1 # int | The maximum number of records to return. (optional) (default to 25)
  offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
  fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)
  
  try: 
      # Search Endpoint
      api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
      pprint(api_response.data)
      common.send_message("*" + q + "*", api_response.data[0].images.original.url)
  except ApiException as e:
      print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

def weather(message, param):
  if not param:
      param = config.bot['weather']['default_location']
  r = requests.get('http://wttr.in/' + param + "?1n")
  buienradar_url = 'https://api.buienradar.nl/image/1.0/RadarMapBE?w=500&h=512&time=' + str(int(time.time()))
  if r.text:
    # we get text in ANSI, escape it
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    common.send_message("```\n" + ansi_escape.sub('', r.text) + "\n```", buienradar_url)
    return 0
  common.send_message("*Current weather in BE:*", buienradar_url)


def help(message, param):
  global commands
  common.send_message("Available commands:\n" + "\n".join(list(commands.keys())))

def parse(message):
  global commands
  commands = {'!test': test,
              '!ping': ping,
              '!ddg': ddg,
              '!gif': gif,
              '!help': help,
              '!weather': weather,
  }

  is_command = re.match('^\!(.+)', message['messages'][0]['msg'])
  command = message['messages'][0]['msg'].partition(' ')[0]

  if is_command and command in commands:
    param = ' '.join(message['messages'][0]['msg'].split()[1:])
    commands[command](message, param)
