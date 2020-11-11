from __future__ import annotations

from typing import TYPE_CHECKING, List

from ai.model import PresidentModel
from ai.representation_mapper import map_cards_to_vector, map_vector_to_cards
from game.agent import Agent
from game.player import Player
from game.table import Table

if TYPE_CHECKING:
    from game.card import Card


class DQLAgent(Agent):
    def __init__(self):
        super().__init__(Player())
        self.model = PresidentModel([64])

    def make_move(self, table: Table) -> None:
        """
        TODO: Agent makes a move based on the fact that the hand played has the lowest possible value.
        """
        cards_in_hand_vector: List[int] = map_cards_to_vector(self.player.hand)
        cards_previous_move_vector: List[int] = map_cards_to_vector(table.last_move()[0] if table.last_move() else [])
        all_played_cards_vector: List[int] = map_cards_to_vector(
            [y for ys in table.played_cards for y in map(lambda x: x[0], ys)])  # TODO flatmap and add discard_pile

        calculated_move: List[int] = self.model.calculate_next_move(
            cards_in_hand_vector, cards_previous_move_vector, all_played_cards_vector)
        move: List[Card] = map_vector_to_cards(calculated_move, self.player.hand)

        table.try_move(self, move)

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)
