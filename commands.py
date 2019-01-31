import re, sys
from pprint import pprint

import config
import common

sys.path.append('duckduckgo')
import DuckDuckGo


def test(message, param):
  common.send_message('This is a reply to the !test command!')

def ping(message, param):
  common.send_message('Pong!')

def ddg(message, param):
  q = DuckDuckGo.search(param)
  if q.abstract.abstract:
    common.send_message("*" + q.abstract.heading + "*:\n" + q.abstract.abstract_text + "\n" + q.abstract.abstract_url)
  elif q.definition.definition:
    common.send_message("*" + param  + "*:\n" + q.definition.definition)
  elif q.answer.answer:
    common.send_message("*" + param  + "*:\n" + q.answer.answer)
  elif q.results:
    common.send_message("*" + param  + "*:\n" + q.results[0].text + "\n" + q.results[0].first_url)
  elif q.related_topics:
    common.send_message("*" + param  + "*:\n" + q.related_topics[0].text + "\n" + q.related_topics[0].first_url)
  else:
    common.send_message("I couldn't find anything for _" + param + "_!")

def parse(message):
  commands = {'!test': test,
              '!ping': ping,
              '!ddg': ddg,
  }

  is_command = re.match('^\!(.+)', message['messages'][0]['msg'])
  command = message['messages'][0]['msg'].partition(' ')[0]

  if is_command and command in commands:
    param = ' '.join(message['messages'][0]['msg'].split()[1:])
    commands[command](message, param)
