from random import shuffle
from typing import List

from game.card import *
from game.settings import *


class Deck:
    """Just a collection of cards, with some functions to ease things. No game specific implementations."""

    def __init__(self):
        self.card_stack = []
        self.played_cards = []
        self.playing_per_amount = 1
        self.reset_cards_stack()

    def reset_cards_stack(self):
        """
        Reset the card stack. Clear all cards and add a fresh (shuffled) set.
        """
        self.card_stack.clear()
        for symbol, value in CARD_VALUES:
            for suit in Suit:
                self.card_stack.append(Card(value, suit, suit.get_color() + " " + symbol + " of " + suit))
        shuffle(self.card_stack)

    def divide(self, nr_players: int) -> List[List[Card]]:
        """
        Shuffle and Divide all cards in as there are players, indicated by nr_players
        """
        shuffle(self.card_stack)
        result = [[] for _ in range(nr_players)]
        for i in range(len(self.card_stack)):
            result[i % nr_players].append(self.card_stack[i])
        return result
