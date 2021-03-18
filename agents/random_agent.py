from __future__ import annotations

import random
from typing import TYPE_CHECKING, List

from game.agent import Agent
from game.player import Player
from game.table import Table

if TYPE_CHECKING:
    from game.card import Card


class RandomAgent(Agent):
    def __init__(self, player_name: str = None):
        super().__init__(Player(player_name if player_name is not None else 'RandomAgent'))

    async def make_move(self, table: Table) -> None:
        """
        Let the agent make a random move from all possible moves in his state.
        """
        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)
        table.try_move(self, random.choice(possible_moves))

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in random order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        random.shuffle(possible_cards)
        return possible_cards
