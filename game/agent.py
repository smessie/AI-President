from __future__ import annotations

from typing import TYPE_CHECKING, List

from game.player import Player

if TYPE_CHECKING:
    from game.card import Card
    from game.table import Table


class Agent:
    def __init__(self, player: Player):
        self.player: Player = player

    async def make_move(self, table: Table) -> None:
        """
        This function is called when the agent should make a move.
        table.make_move() should be called, this makes the move and returns a reward.
        """
        pass

    async def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Function used by President to exchange cards at the beginning of a round. Most wanted card should be in front.
        """
        return sorted(table.deck.card_stack, reverse=True)

    async def get_card_for_scum(self) -> Card:
        """
        Function used by President to exchange cards at the beginning of a round. Card to give to the scum should be
        returned.
        """
        return sorted(self.player.hand)[0]

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        """
        Called when a round ends.
        """
        pass

    async def game_end_callback(self, game_nr: int) -> bool:
        """
        Called when a game ends.

        Returns true if agent wants to early stop.
        """
        return False

    def move_played_callback(self, move: List[Card], player: Player):
        """
        Called when any player makes a move.
        """
        pass

    def trick_end_callback(self, table: Table, playing_agents: List[Agent]):
        """
        Called when trick is ended and new one begins.
        """
        pass

    def cards_divided_callback(self):
        """
        Called when the cards are divided.
        """
        pass

    def cards_exchanged_callback(self):
        """
        Called when the cards are exchanged.
        """
        pass
