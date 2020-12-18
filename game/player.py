from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game.agent import Agent
    from game.card import Card
    from game.table import Table


class Player:
    _player_id: int = 0

    def __init__(self, name: str = None):
        self.hand: List[Card] = []
        self.player_id: int = int(Player._player_id)
        Player._player_id += 1
        self.player_name = name if name is not None else 'Nameless'

    def get_all_possible_moves(self, table: Table, agent: Agent) -> List[List[Card]]:
        possible_moves = [[]] if table.played_cards else []
        for amount_of_cards in range(len(table.last_move()[0]) if table.last_move() else 1, len(self.hand) + 1):
            for potential_move in combinations(self.hand, amount_of_cards):
                if table.game.valid_move(list(potential_move), agent):
                    possible_moves.append(list(potential_move))
        return possible_moves

    def get_player_id(self):
        return self.player_id

    def get_player_name(self):
        return self.player_name

    def __eq__(self, other):
        return self.player_id == other.get_player_id()
