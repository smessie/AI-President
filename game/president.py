from __future__ import annotations

from typing import List, Iterator, Tuple, Optional, TYPE_CHECKING

from tqdm import tqdm

from game.table import Table
from util.iterator import CustomIterator

if TYPE_CHECKING:
    from game.agent import Agent
    from game.card import Card


class President:
    """
    A class containing the game logic.
    """

    def __init__(self, agents: List[Agent]):
        self.agents: List[Agent] = agents
        self.agent_iterator: CustomIterator = CustomIterator(agents)
        self.table = Table(self)

    def play(self, games: int, rounds: int) -> None:
        """
        Start the game. Play a certain amount of games each consisting of a certain amount of rounds.
        """
        progress = tqdm(total=games * rounds)

        for g in range(games):
            for r in range(rounds):
                # Update the progress bar
                progress.set_description(f"Running round {r} of game {g}")
                progress.update()

                # Reset from the previous round
                self._reset()

                # Play the round
                for agent in self._get_play_order():
                    agent.make_move(self.table)

        progress.close()

    def on_move(self, agent: Agent, cards: List[Card]) -> Tuple[int, bool]:
        """
        Handle move from Agent, We can be sure the agent can actually play the card.
        return (valid_move, reward, is_final).
        """
        last_move: Tuple[List[Card], Agent] = self.table.last_move()

        # If multiple cards are played the value should be the same and length at least the same.
        if cards and (not all(cards[i].value == cards[0].value for i in range(len(cards))) or
                      (last_move and len(cards) < len(last_move))):
            return -10, False  # TODO fix reward

        if not cards:
            # A Pass, disable the player for this round
            agent.player.passed = True
            return -5, False  # TODO fix reward

        # Check that each played card in the trick has the same rank, or if not, it is a 2.
        played_value: Optional[int] = self._get_played_value(cards)
        if not played_value or played_value < 0:
            return -10, False
        last_move_value: int = self._get_played_value(last_move[0]) if last_move else None

        # Previous value should be lower
        if not last_move or last_move_value <= played_value:
            self.table.do_move(agent, cards)
            return 10, False  # TODO fix reward
        else:
            return -10, False  # TODO fix reward

    def _get_played_value(self, cards: List[Card]) -> Optional[int]:
        """
        Get the value of a stack off cards if they are all the same except for some 2s, -1 if not and None if only 2s
        """
        played_value: Optional[int] = None
        for card in cards:
            if card.value != 2:
                if played_value and played_value != card.value:
                    # Cards do not have the same rank
                    return -1
                played_value = card.value
        return played_value

    def _reset(self) -> None:
        """
        - (Re)divide cards
        - reset the playing table
        """
        for i, hand in enumerate(self.table.deck.divide(len(self.agents))):
            self.agents[i].player.hand = hand
            self.agents[i].player.position = None
        self.table.reset()

    def _get_play_order(self) -> Iterator[Agent]:
        """
        Return the player order, this is an iterator so this allows for cleaner code in the President class.
        """
        # As long as there are 2 unfinished players
        while [len(agent.player.hand) > 0 for agent in self.agents].count(True) >= 2:
            self.agent_iterator.next()
            nr_skips: int = 0
            while nr_skips <= len(self.agents) and (
                    len(self.agent_iterator.get().player.hand) == 0 or self.agent_iterator.get().player.passed):
                self.agent_iterator.next()
                nr_skips += 1
            if nr_skips > len(self.agents):
                print('Infinite loop detected while looking for next player.')
                return
            yield self.agent_iterator.get()
