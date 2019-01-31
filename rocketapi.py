#!/usr/bin/env python
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

rocket_api_session = None

def create_session(user = None, password = None, server_url = None):
    global rocket_api_session

    if not rocket_api_session:
        rocket_api_session = RocketChat(user, password, server_url)

    pprint(rocket_api_session.me().json())
    return rocket_api_session
