from random import shuffle
from typing import List

from game.card import Card, Suit
from game.settings import CARD_VALUES


class Deck:
    """Just a collection of cards, with some functions to ease things. No game specific implementations."""

    def __init__(self):
        self.card_stack: List[Card] = []
        self.reset_cards_stack()

    def reset_cards_stack(self) -> None:
        """
        Reset the card stack. Clear all cards and add a fresh (shuffled) set.
        """
        self.card_stack.clear()
        for symbol in CARD_VALUES:
            for suit in Suit:
                self.card_stack.append(
                    Card(CARD_VALUES[symbol], suit, str(suit.get_color()) + " " + symbol + " of " + str(suit)))
        shuffle(self.card_stack)
