#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import discord

from boulet_bot.models.user import User

def load_commands(bot):
    # ----- COMMANDS ----- #

    @bot.command(name='hello', pass_context=True)
    async def hello(context):
        msg = 'Hello {author}'.format(author=context.message.author.mention)
        await bot.say(msg)


    @bot.command(name='fun', pass_context=True)
    async def fun(context):
        msg = bot.gifs['dance']
        await bot.say(msg)


    @bot.command(name='setboulet', pass_context=True)
    async def setboulet(context, username: discord.User=None, boulet=None):
        if username and boulet:
            user = bot.bot.session.query(User).filter(User.name == str(username)).first()
            if user:
                user.boulet = int(boulet)
                bot.session.commit()
                msg = '<@{}> a maintenant {} points boulet !'.format(username.id, user.boulet)
                await bot.say(msg)

    @bot.command(name='boulet', pass_context=True)
    async def boulet(context, boulet_user: discord.User=None):
        role = discord.utils.get(context.message.server.roles, name=bot.boulet_role)

        if boulet_user and not boulet_user.bot:
            if str(boulet_user) != str(context.message.author):

                now = datetime.datetime.now()
                last_boulet = bot.boulet_time.get(str(context.message.author), now - datetime.timedelta(minutes=10))
                delta = now - last_boulet

                if delta.total_seconds() > 0:
                    bot.boulet_time[str(context.message.author)] = now
                    user = bot.session.query(User).filter(User.name == str(boulet_user)).first()

                    if not user:
                        user = User(str(boulet_user))
                        bot.session.add(user)
                    else:
                        user.boulet += 1

                    if user.boulet % 10 == 0:
                        msg = '<@{}> a gagné le rôle de {} pour 24h!'.format(boulet_user.id, bot.boulet_role)
                        user.old_name = boulet_user.display_name
                        user.boulet_date = now + datetime.timedelta(days=1)

                        await bot.add_roles(boulet_user, role)
                        await bot.change_nickname(boulet_user, bot.boulet_role)
                    else:
                        msg = '<@{}> a gagné un point boulet ! [{}]'.format(boulet_user.id, user.boulet)

                    bot.session.commit()

                else:
                    return None

            else:
                return None

        else:
            users = bot.session.query(User).order_by(User.boulet.desc()).all()
            msg = "#---------BOULETS SCORES---------#\n\n"
            count = 1
            for user in users:
                msg += " # {} - [{}] {}\n".format(count, user.boulet, user.name)

                count += 1

        await bot.say(msg)

    # ----- EVENTS ----- #

    @bot.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == bot.user:
            return

        if str(message.channel) != "command-bot":
            return

        if message.content.startswith('!beintelligent'):
            msg = 'Yeah! Science bitch!'
            await bot.send_message(message.channel, msg)

        else:
            await bot.process_commands(message)


    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(game=discord.Game(name="chercher du gras"))
