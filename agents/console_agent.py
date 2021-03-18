from __future__ import annotations

from typing import TYPE_CHECKING, List

from colorama import Fore, Style, init

from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import print_cards

if TYPE_CHECKING:
    from game.card import Card

init()  # Required for colorama


def print_whitespace():
    print('')
    print('-' * 40)
    print('')


class ConsoleAgent(Agent):
    def __init__(self, player_name: str = None):
        super().__init__(Player(player_name if player_name is not None and player_name != '' else 'ConsoleAgent'))

    async def make_move(self, table: Table) -> None:
        print_whitespace()

        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)
        for i, move in enumerate(possible_moves):
            print(f'Move {Style.BRIGHT}{i}{Style.NORMAL}:')
            print_cards(move)

        print("Your cards:")
        print_cards(sorted(self.player.hand, key=lambda x: x.value))

        move = int(input('Enter move_nr to take: '))
        while not 0 <= move < len(possible_moves):
            print(f'{Fore.RED}Move {move} is invalid! Try again.{Fore.RESET}')
            move = int(input('Enter move_nr to take: '))
        table.try_move(self, possible_moves[move])

    def move_played_callback(self, move: List[Card], player: Player):
        if move:
            print(f'{player.get_player_name()} made following move and has {Style.BRIGHT}{len(player.hand)}'
                  f'{Style.NORMAL} cards left:')
            print_cards(move)
        else:
            print(f'{player.get_player_name()} passed.')

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        print_whitespace()
        print(f'{Fore.BLUE}Round has ended! Here is the ranking:{Fore.RESET}')
        for i, agent in enumerate(agent_finish_order):
            prefix = ''
            if agent == self:
                prefix = f"{Fore.BLUE}"
            print(f'{prefix}#{i + 1}. {agent.player.get_player_name()}{Fore.RESET}')
        print_whitespace()

    async def game_end_callback(self, game_nr: int) -> bool:
        print_whitespace()
        print('Aww, the game is already over :(')
        keep_playing = input('Lets play another game? (y/n)').lower().strip()
        while keep_playing != 'y' and keep_playing != 'n':
            keep_playing = input('Uhh what did you say? Lets play another game? (y/n)').lower().strip()
        return keep_playing == 'n'

    def trick_end_callback(self, table: Table, playing_agents: List[Agent]):
        print(f'{Fore.YELLOW}Let\'s clear the deck. On to the next trick! '
              f'{", ".join(map(lambda agent: agent.player.get_player_name(), playing_agents))} are still playing.'
              f'{Fore.RESET}')
