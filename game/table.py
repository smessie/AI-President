from typing import List, Tuple, Optional

from game.agent import Agent
from game.card import Card
from game.deck import Deck
from game.president import President


class Table:
    def __init__(self, game: President):
        self.game = game
        self.current: int = 0
        self.deck = Deck()
        self.played_cards: List[Tuple[List[Card], Agent]] = []
        self.discard_pile: List[List[Card]] = []

    def reset(self) -> None:
        """
        Reset the table:
        - reset played_cards
        - reset discard_pile
        """
        self.played_cards.clear()
        self.discard_pile.clear()

    def new_trick(self) -> None:
        """
        Move the cards from the played_cards to the discard_pile.
        """
        self.discard_pile += self.played_cards
        self.played_cards.clear()

    def make_move(self, agent: Agent, cards: List[Card]) -> Tuple[int, bool]:
        """
        Take a move from an agent, execute the move on the table and give a reward to the agent.
        Validate if the move is valid first.

        TODO: discuss this.
        TODO: move rewards to settings file.
        Reward scheme:
        - Invalid move: -10
        - else return game specific reward

        return the reward and if the move is final.
        """
        # A pass is a valid move.
        if len(cards) != 0:
            # WARNING: when playing with 2 decks of cards this is not sufficient.
            if not all(card in agent.player.hand for card in cards):
                return -10, False

        # At this point we know the card is valid, pass the move to the game logic.
        valid, reward, final = self.game.on_move(agent, cards)[1:]

        # The move is valid, the cards can be moved from the players hand to the table.
        if valid:
            [agent.player.hand.remove(card) for card in cards]
            self.played_cards.append((cards, agent))

        return reward, final

    def last_move(self) -> Optional[Tuple[List[Card], Agent]]:
        return self.played_cards[-1] if len(self.played_cards) > 0 else None
