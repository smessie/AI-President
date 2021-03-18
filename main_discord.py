#!/usr/bin/env python3
import asyncio
from threading import Thread

from discordbot.discord_bot import DiscordBot

if __name__ == "__main__":
    discord_bot = DiscordBot()
    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.start(input('Enter bot token: ')))
    loop.create_task(discord_bot.print_task())
    loop.create_task(discord_bot.run_game())
    thread = Thread(target=loop.run_forever, args=())
    thread.start()
