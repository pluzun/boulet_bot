#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import datetime
import discord

from boulet_bot.models.user import User


async def remove_outdated_boulets(bot):
    print('Starting daemon')
    while True:
        await asyncio.sleep(30)

        users = bot.session.query(User).all()
        outdated_boulets = []

        if len(bot.servers) > 0:
            servers = bot.servers
            for server in servers:
                if str(server) == 'La Casa Del Gro':
                    break
        else:
            continue

        now = datetime.datetime.now()
        role = discord.utils.get(server.roles, name=bot.boulet_role)

        for user in users:
            if user.boulet_date and user.boulet_date < now:
                for server_user in server.members:
                    if user.name == str(server_user):
                        print('{} is not boulet anymore'.format(server_user))
                        await bot.remove_roles(server_user, role)
                        await bot.change_nickname(server_user, user.old_name)
                        user.boulet_date = None
                        bot.session.commit()
