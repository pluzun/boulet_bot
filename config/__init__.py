#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def get_config():
    with open('./config.json') as config_file:
        config = json.loads(config_file.read())

    return config


configurations = get_config()

token = configurations.get('discord_token', None)
bot_prefix = configurations.get('bot_prefix', '!')
boulet_role = configurations.get('boulet_role', 'boulet')
