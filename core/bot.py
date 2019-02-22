#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord.ext.commands import Bot

from boulet_bot.config.db import Session

from .commands import load_commands


class BouletBot(Bot):
        
    def __init__(self, bot_prefix, boulet_role, token):
        Bot.__init__(self, command_prefix=bot_prefix)
        self.boulet_role = boulet_role
        self.boulet_time = {}
        gifs = {
            "dance": "https://gph.is/2GPipKH",
        }
        self.session = Session()
        self.token = token
        load_commands(self)
        self.run(token)
