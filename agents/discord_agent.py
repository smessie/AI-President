from __future__ import annotations

import asyncio
from threading import Thread
from typing import TYPE_CHECKING, List

from discordbot.discord_bot import DiscordBot
from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import print_cards_string

if TYPE_CHECKING:
    from game.card import Card


class DiscordAgent(Agent):
    def __init__(self, player_name: str = None):
        super().__init__(Player(player_name if player_name is not None and player_name != '' else 'DiscordAgent'))
        self.discord_bot = DiscordBot()
        loop = asyncio.get_event_loop()
        loop.create_task(self.discord_bot.start(input('Enter bot token: ')))
        loop.create_task(self.discord_bot.print_task())
        thread = Thread(target=loop.run_forever, args=())
        thread.start()

    def make_move(self, table: Table) -> None:
        self.print_whitespace()

        to_print = ''
        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)
        for i, move in enumerate(possible_moves):
            to_print += f'Move {i}:\n'
            move_string = 'PASS\n\n' if move == [] else print_cards_string(move)
            if len(to_print) + len(move_string) > 1950:
                self.discord_bot.print(to_print)
                to_print = ''
            to_print += move_string

        to_print += 'Your cards:\n'
        move_string = print_cards_string(sorted(self.player.hand, key=lambda x: x.value))
        if len(to_print) + len(move_string) > 1950:
            self.discord_bot.print(to_print)
            to_print = ''
        to_print += move_string
        self.discord_bot.print(to_print)

        move = self.discord_bot.read_int_input('Enter move_nr to take: ')
        while not 0 <= move < len(possible_moves):
            self.discord_bot.print(f'Move {move} is invalid! Try again.')
            move = self.discord_bot.read_int_input('Enter move_nr to take: ')
        table.try_move(self, possible_moves[move])

    def move_played_callback(self, move: List[Card], player: Player):
        if move:
            to_print = ''
            to_print += f'{player.get_player_name()} made following move and has {len(player.hand)} cards left:\n'
            to_print += print_cards_string(move)
            self.discord_bot.print(to_print)
        else:
            self.discord_bot.print(f'{player.get_player_name()} passed.')

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        self.print_whitespace()
        to_print = '**Round has ended! Here is the ranking:**\n'
        for i, agent in enumerate(agent_finish_order):
            to_print += f'**#{i + 1}. {agent.player.get_player_name()}**\n'
        self.discord_bot.print(to_print)
        self.print_whitespace()

    def game_end_callback(self, game_nr: int) -> bool:
        self.print_whitespace()
        self.discord_bot.print('Aww, the game is already over :(')
        keep_playing = self.discord_bot.read_bool_input('Lets play another game? (y/n)')
        return not keep_playing

    def trick_end_callback(self, table: Table, playing_agents: List[Agent]):
        self.discord_bot.print(f'Let\'s clear the deck. On to the next trick! '
                               f'{", ".join(map(lambda agent: agent.player.get_player_name(), playing_agents))}'
                               f' are still playing.')

    def print_whitespace(self):
        self.discord_bot.print('- \n' + ('-' * 40) + '\n- \n')
