#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord.ext.commands import Bot

from boulet_bot.config.db import Session

from .commands import load_commands
from .daemon import remove_outdated_boulets


class BouletBot(Bot):
        
    def __init__(self, bot_prefix, boulet_interval, boulet_role, token):
        Bot.__init__(self, command_prefix=bot_prefix)
        self.boulet_role = boulet_role
        self.boulet_time = {}
        self.gifs = {
            "dance": "https://gph.is/2GPipKH",
        }
        self.session = Session()
        self.token = token
        self.boulet_interval = boulet_interval
        load_commands(self)
        self.loop.create_task(remove_outdated_boulets(self))
        self.run(token)
