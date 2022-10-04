#!/usr/bin/env python3
import asyncio
import sys
from threading import Thread

import discord

from discordbot.discord_bot import DiscordBot

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True

    discord_bot = DiscordBot()
    loop = asyncio.get_event_loop()
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("Enter token: ")
    loop.create_task(discord_bot.start(token))
    loop.create_task(discord_bot.print_task())
    loop.create_task(discord_bot.run_game())
    thread = Thread(target=loop.run_forever, args=())
    thread.start()
    thread.join()
