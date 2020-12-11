from __future__ import annotations

from typing import TYPE_CHECKING, List

from game.player import Player

if TYPE_CHECKING:
    from game.card import Card
    from game.table import Table


class Agent:
    def __init__(self, player: Player):
        self.player: Player = player

    def make_move(self, table: Table) -> None:
        """
        This function is called when the agent should make a move.
        table.make_move() should be called, this makes the move and returns a reward.
        """
        pass

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Function used by President to exchange cards at the beginning of a round. Most wanted card should be in front.
        """
        return sorted(table.deck.card_stack, reverse=True)

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        """
        Called when a round ends.
        """
        pass

    def game_end_callback(self, game_nr: int) -> bool:
        """
        Called when a game ends.

        Returns true if agent wants to early stop.
        """
        pass
