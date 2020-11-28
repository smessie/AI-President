from __future__ import annotations

from typing import TYPE_CHECKING, List

from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import print_cards

if TYPE_CHECKING:
    from game.card import Card


class ConsoleAgent(Agent):
    def __init__(self):
        super().__init__(Player())

    def make_move(self, table: Table) -> None:
        print('-' * 40)
        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)
        for i, move in enumerate(possible_moves):
            print(f'Move {i}:')
            print_cards(move)
        move = int(input('Enter move_nr to take: '))
        while not 0 <= move <= len(possible_moves):
            move = int(input('Enter move_nr to take: '))
        table.try_move(self, possible_moves[move])
