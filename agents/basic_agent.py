from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import get_played_value

if TYPE_CHECKING:
    from game.card import Card


class BasicAgent(Agent):
    def __init__(self):
        super().__init__(Player())

    def make_move(self, table: Table) -> None:
        """
        Agent makes a move based on the fact that the hand played has the lowest possible value.
        """
        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)

        smallest_move = possible_moves[0]
        smallest_move_value: Optional[int] = get_played_value(smallest_move)
        for move in possible_moves:
            move_value: Optional[int] = get_played_value(move)
            if move_value and (not smallest_move_value or move_value > smallest_move_value):
                smallest_move_value = move_value
                smallest_move = move
        table.try_move(self, smallest_move)

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)
