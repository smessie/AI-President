from itertools import cycle
from typing import List, Iterator, Tuple

from tqdm import tqdm

from game.agent import Agent
from game.card import Card
from game.table import Table
from util.iterator import CustomIterator


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
        TODO return game results
        """
        progress = tqdm(total=games*rounds)

        for g in range(games):
            for r in range(rounds):
                # Update the progress bar
                progress.set_description(f"Running round {r} of game {g}.")
                progress.update()

                # Reset from the previous round
                self.reset()

                # Play the round
                for agent in self.get_play_order():
                    agent.make_move(self.table)

        progress.close()

    def on_move(self, agent: Agent, cards: List[Card]) -> Tuple[bool, int, bool]:
        """
        Handle move from Agent, We can be sure the agent can actually play the card.
        return (valid_move, reward, is_final).
        """
        return True, 0, False

    def reset(self) -> None:
        """
        - (Re)divide cards
        - reset the playing table
        """
        for i, hand in enumerate(self.table.deck.divide(len(self.agents))):
            self.agents[i].player.hand = hand
            self.agents[i].player.position = None
        self.table.reset()

    def get_play_order(self) -> Iterator[Agent]:
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
            yield self.agent_iterator.get()
