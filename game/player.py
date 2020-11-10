from __future__ import annotations

from itertools import combinations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import Card
    from game.table import Table


class Player:
    _player_id: int = 0

    def __init__(self):
        self.hand: List[Card] = []
        self.player_id: int = Player._player_id
        Player._player_id += 1

    def get_all_possible_moves(self, table: Table) -> [[Card]]:
        possible_moves = []
        for amount_of_cards in range(len(table.last_move()[0]) if table.last_move() else 1, len(self.hand) + 1):
            for potential_move in combinations(self.hand, amount_of_cards):
                if table.game.valid_move(list(potential_move)):
                    possible_moves.append(list(potential_move))
        return possible_moves
