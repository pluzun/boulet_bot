#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import discord

from discord.ext.commands import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import User

from config import bot_prefix, token, boulet_role
from config.db import Session, engine, Base


GIFS = {
    "dance": "https://gph.is/2GPipKH",
}
BOULET_TIME = {}

Base.metadata.create_all(engine)
session = Session()

bot = Bot(command_prefix=bot_prefix)


@bot.command(name='hello', pass_context=True)
async def hello(context):
    msg = 'Hello {author}'.format(author=context.message.author.mention)
    await bot.say(msg)


@bot.command(name='fun', pass_context=True)
async def fun(context):
    msg = GIFS['dance']
    await bot.say(msg)


@bot.command(name='setboulet', pass_context=True)
async def setboulet(context, username: discord.User=None, boulet=None):
    if username and boulet:
        user = session.query(User).filter(User.name == str(username)).first()
        if user:
            user.boulet = int(boulet)
            session.commit()
            msg = '<@{}> a maintenant {} points boulet !'.format(username.id, user.boulet)
            await bot.say(msg)



@bot.command(name='boulet', pass_context=True)
async def boulet(context, username: discord.User=None):
    role = discord.utils.get(context.message.server.roles, name=boulet_role)

    if username and not username.bot:
        if str(username) != str(context.message.author):

            now = datetime.datetime.now()
            last_boulet = BOULET_TIME.get(str(context.message.author), now - datetime.timedelta(minutes=10))
            delta = now - last_boulet

            if delta.total_seconds() > 120:
                BOULET_TIME[str(context.message.author)] = now
                user = session.query(User).filter(User.name == str(username)).first()

                if not user:
                    user = User(str(username))
                    session.add(user)
                else:
                    user.boulet += 1

                if user.boulet % 10 == 0:
                    msg = '<@{}> a gagné le rôle de {} pour 24h!'.format(username.id, boulet_role)
                    await bot.add_roles(username, role)
                    await bot.change_nickname(username, boulet_role)

                    user.boulet_date = now + datetime.timedelta(days=1)
                else:
                    msg = '<@{}> a gagné un point boulet ! [{}]'.format(username.id, user.boulet)

                session.commit()

            else:
                return None

        else:
            return None

    else:
        users = session.query(User).order_by(User.boulet.desc()).all()
        msg = "#---------BOULETS SCORES---------#\n\n"
        count = 1
        for user in users:
            msg += " # {} - [{}] {}\n".format(count, user.boulet, user.name)

            count += 1

    await bot.say(msg)


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

bot.run(token)
