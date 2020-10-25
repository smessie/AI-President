from random import shuffle
from typing import List

from game.Card import *
from game.settings import *


class Deck:
    """Just a collection of cards, with some functions to ease things. No game specific implementations."""

    def __init__(self):
        self.card_stack = []
        self.played_cards = []
        self.playing_per_amount = 1

        # initialize the card stack
        for symbol, value in CARD_VALUES:
            for suit in Suit:
                self.card_stack.append(Card(value, suit, suit.get_color() + " " + symbol + " of " + suit))
        shuffle(self.card_stack)

    # todo: this belongs in the President Class
    def is_valid_play(self, cards: List[Card]):
        """"Check if the given card(s) can be played based on the current state of the game."""

        # Check that there are more or the same amount of cards played.
        if len(cards) < self.playing_per_amount:
            return False

        # Check that each played card in the trick has the same rank, or if not, it is a 2.
        played_value = None
        for card in cards:
            if card.value is not 2:
                if played_value is not None and played_value != card.value:
                    return False
                played_value = card.value

        # Check that not only twos were played.
        if played_value is None:
            return False

        # Check that the played cards are of the same or higher rank.
        previous_card = self.get_latest_hand()
        representative_card = None
        for card in cards:
            if card.value is not 2 and (representative_card is None or card > representative_card):
                representative_card = card
        return previous_card is None or representative_card >= previous_card

    def get_latest_hand(self):
        """Return the highest card of the previous played hand (eg. red is higher than black)."""
        if not self.played_cards:
            return None
        card = None
        for i in range(1, self.playing_per_amount + 1):
            potential_card = self.played_cards[-i]
            if potential_card.value is not 2:
                if card is None or potential_card > card:
                    card = potential_card
        return card
