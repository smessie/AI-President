import asyncio

import discord

from agents.better_agent import BetterAgent
from agents.discord_agent import DiscordAgent
from agents.dql_agent import DQLAgent
from agents.random_agent import RandomAgent
from game.president import President

client = discord.Client()


class DiscordBot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.waiting_for_input = []
        self.input_message = {}
        self.game_channel = None
        self.print_queue = []
        self.game_channels = []
        self.starting_members = []

    @client.event
    async def on_ready(self):
        print('Logged on as', self.user)

    @client.event
    async def on_message(self, message):
        channel = message.channel
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await channel.send('Hello!')

        if message.content.startswith('start'):
            if self.game_channel is None:
                self.game_channel = channel
                await message.channel.send('Game channel set!')
            else:
                await channel.send('Starting a new game...')
                mentions = message.mentions
                if not mentions:
                    await channel.send('Mention all players including yourself for which you want to start a game.')
                    return

                self.starting_members = mentions
            return

        if channel not in self.game_channels:
            return

        if channel in self.waiting_for_input and channel not in self.input_message:
            self.input_message[channel] = message.content

    async def read_string_input(self, message: str, channel) -> str:
        self.waiting_for_input.append(channel)
        self.print_queue.append((channel, message))
        await asyncio.sleep(1)

        message = None
        while message is None:
            while channel not in self.input_message:
                # Wait
                await asyncio.sleep(1)
            if self.input_message[channel] is not None:
                message = self.input_message[channel]
        self.waiting_for_input.remove(channel)
        del self.input_message[channel]
        return message

    async def read_int_input(self, message: str, channel) -> int:
        self.waiting_for_input.append(channel)
        self.print_queue.append((channel, message))
        await asyncio.sleep(1)

        move = -1
        while move == -1:
            while channel not in self.input_message:
                # Wait
                await asyncio.sleep(1)
            if self.input_message[channel] is not None:
                try:
                    move = int(self.input_message[channel])
                except ValueError:
                    del self.input_message[channel]
        self.waiting_for_input.remove(channel)
        del self.input_message[channel]
        return move

    async def read_bool_input(self, message: str, channel) -> bool:
        self.waiting_for_input.append(channel)
        self.print_queue.append((channel, message))
        await asyncio.sleep(1)

        bool_value = None
        while bool_value is None:
            while channel not in self.input_message:
                # Wait
                await asyncio.sleep(1)
            if self.input_message[channel] is not None:
                if self.input_message[channel].lower().startswith('y'):
                    bool_value = True
                    self.print_queue.append((channel, "Alright :)"))
                elif self.input_message[channel].lower().startswith('n'):
                    bool_value = False
                    self.print_queue.append((channel, "Alright :("))
                else:
                    del self.input_message[channel]
                    self.print_queue.append((channel, message))
        self.waiting_for_input.remove(channel)
        del self.input_message[channel]
        return bool_value

    def print(self, message: str, channel):
        n = 2000
        for i in range(0, len(message), n):
            self.print_queue.append((channel, message[i:i + n]))

    async def print_task(self):
        while self.game_channel is None:
            # Wait
            await asyncio.sleep(1)
        while True:
            for channel, message in self.print_queue:
                await channel.send(message)
            self.print_queue = []
            await asyncio.sleep(1)

    async def run_game(self):
        while True:
            while not self.starting_members:
                # Wait
                await asyncio.sleep(1)
            guild = self.game_channel.guild
            agents = []
            for member in self.starting_members:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await guild.create_text_channel(f'game-{member.display_name}', overwrites=overwrites)
                self.game_channels.append(channel)
                await channel.send(f'Hi {member.mention}, this is your channel during this game. Good luck!')
                agent = DiscordAgent(discord_bot=self, channel=channel, player_name=member.display_name)
                agents.append(agent)

            self.starting_members = []

            if len(agents) < 4:
                agents.append(DQLAgent(
                    buffer_capacity=2000,
                    hidden_layers=[78, 260],
                    load_checkpoint=True,
                    batch_size=100,
                    epsilon=5,
                    lower_eps_over_time=0,
                    track_training_loss=True,
                    living_reward=-0.1,
                    training_mode=False,
                    filepath="data/saves/10/training-0/cp.ckpt",
                    csv_filepath="data/saves/10/results/wins-benchmark.csv"
                ))
            if len(agents) < 4:
                agents.append(BetterAgent('Betty'))
            if len(agents) < 4:
                agents.append(RandomAgent('Randy'))

            game = President(agents)

            await asyncio.sleep(1)

            # Start the game
            await game.play(10, 1, 0, sleep_in_between=True)

            await asyncio.sleep(1)

            # Print leaderboard
            await self.game_channel.send('- \n' + ('-' * 40) + '\n- \n')
            to_print = '**Game has ended! Here is the ranking:**\n'
            for i, agent in enumerate(game.agent_finish_order):
                to_print += f'**#{i + 1}. {agent.player.get_player_name()}**\n'
            n = 2000
            for i in range(0, len(to_print), n):
                await self.game_channel.send(to_print[i:i + n])
            await self.game_channel.send('- \n' + ('-' * 40) + '\n- \n')

            # Clean up the game channels
            for channel in self.game_channels:
                await channel.delete()
            self.game_channels = []
