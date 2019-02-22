#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import bot_prefix, boulet_role, token
from core.bot import BouletBot

bot = BouletBot(bot_prefix, boulet_role, token)
bot.start()
