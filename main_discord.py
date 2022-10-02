#!/usr/bin/env python3
import asyncio
from threading import Thread

import discord

from discordbot.discord_bot import DiscordBot

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True

    discord_bot = DiscordBot()
    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.start(input('Enter bot token: ')))
    loop.create_task(discord_bot.print_task())
    loop.create_task(discord_bot.run_game())
    thread = Thread(target=loop.run_forever, args=())
    thread.start()
    thread.join()
