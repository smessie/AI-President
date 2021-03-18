from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import get_played_value

if TYPE_CHECKING:
    from game.card import Card


class BetterAgent(Agent):
    def __init__(self, player_name: str = None):
        super().__init__(Player(player_name if player_name is not None else 'BetterAgent'))

    async def make_move(self, table: Table) -> None:
        """
        Agent makes a move based on the fact that the hand played has the lowest possible value.
        """
        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)

        hand_size = len(self.player.hand)
        best_move = possible_moves[0]
        best_move_value: Optional[int] = get_played_value(best_move)
        best_move_size: int = len(best_move)
        for move in possible_moves:
            move_value: Optional[int] = get_played_value(move)
            move_size: int = len(move)
            if move_value and move_value > 0 and (not best_move_value or (
                    move_value < 10 and move_size > best_move_size) or (
                                                          move_value < best_move_value
                                                          and move_size >= best_move_size)) and (
                    hand_size < 7 or 15 not in [card.value for card in move]):
                best_move_value = move_value
                best_move = move
                best_move_size = move_size
        table.try_move(self, best_move)

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)
