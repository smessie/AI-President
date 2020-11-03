from typing import List

from game.agent import Agent
from game.card import Card
from game.table import Table


class Game:
    """
    A class containing the game logic.
    """

    def __init__(self, agents: List[Agent]):
        self.agents: List[Agent] = agents
        self.table = Table(self)

    def play(self) -> None:
        """
        TODO return game results
        """
        for agent in self.table.get_play_order():
            pass  # play move

    def on_move(self, agent: Agent, cards: List[Card]) -> (int, bool):
        """
        Handle move from Agent, We can be sure the agent can actually play the card.
        return the reward and if the move is final.
        """
        return 0, False

    def reset(self):
        """
        - (Re)divide cards
        - reset the playing table
        """
        [agent.player.reset_hand() for agent in self.agents]
        for i, hand in enumerate(self.table.deck.divide(len(self.agents))):
            self.agents[i].player.hand = hand
