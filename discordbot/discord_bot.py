import asyncio

import discord

client = discord.Client()


class DiscordBot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.waiting_for_input = False
        self.input_message = None
        self.game_channel = None
        self.print_queue = []

    @client.event
    async def on_ready(self):
        print('Logged on as', self.user)

    @client.event
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if message.content == 'start' and self.game_channel is None:
            self.game_channel = message.channel
            return

        if message.channel != self.game_channel:
            return

        if self.waiting_for_input and self.input_message is None:
            self.input_message = message.content

    def read_int_input(self, message: str) -> int:
        self.waiting_for_input = True
        self.print_queue.append(message)

        move = -1
        while move == -1:
            while self.input_message is None:
                # Wait
                pass
            if self.input_message is not None:
                try:
                    move = int(self.input_message)
                except ValueError:
                    self.input_message = None
        self.waiting_for_input = False
        self.input_message = None
        return move

    def read_bool_input(self, message: str) -> bool:
        self.waiting_for_input = True
        self.print_queue.append(message)

        bool_value = None
        while bool_value is None:
            while self.input_message is None:
                # Wait
                pass
            if self.input_message is not None:
                if self.input_message.startswith('y'):
                    bool_value = True
                elif self.input_message.startswith('n'):
                    bool_value = False
        self.waiting_for_input = False
        self.input_message = None
        return bool_value

    def print(self, message: str):
        n = 2000
        for i in range(0, len(message), n):
            self.print_queue.append(message[i:i + n])

    async def print_task(self):
        while self.game_channel is None:
            # Wait
            await asyncio.sleep(1)
        while True:
            for message in self.print_queue:
                await self.game_channel.send(message)
            self.print_queue = []
            await asyncio.sleep(1)
