from typing import List, Iterator, Tuple

from tqdm import tqdm

from game.agent import Agent
from game.card import Card
from game.table import Table


class President:
    """
    A class containing the game logic.
    """

    def __init__(self, agents: List[Agent]):
        self.agents: List[Agent] = agents
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
        pass
