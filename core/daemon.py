#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread


class BouletDaemon(Thread):
    def __init__(self):
        Thread.__init__(self, bot)
        self.daemon = True
        self.bot = bot
        self.start()

    def run(self):
        pass
