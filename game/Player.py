from game.Deck import Deck
from game.President import President
from game.Card import Card
from game.Card import Color


class Player:

    def __init__(self, game: President):
        self.cards_in_hand: [Card] = []
        self.game = game

    def move(self, deck: Deck) -> [Card]:
        """Make a move. Empty list makes the player pass."""
        possible_moves = self.get_all_possible_moves(deck)
        return possible_moves[0] if possible_moves else []

    def get_all_possible_moves(self, deck: Deck) -> [[Card]]:
        possible_moves = []
        for i in range(len(self.cards_in_hand) + 1):
            for j in range(i + 1, len(self.cards_in_hand) + 1):
                move = self.cards_in_hand[i:j]
                if len(move) >= deck.playing_per_amount and deck.is_valid_play(move):
                    possible_moves.append(move)
        return possible_moves

    def give_worst_card(self) -> Card:
        worst_card = self.cards_in_hand[0]
        for card in self.cards_in_hand:
            if card.get_value() < worst_card.get_value():
                worst_card = card
        self.cards_in_hand.remove(worst_card)
        return worst_card

    def give_specific_card(self, value: int, color: Color) -> Card or None:
        give_card = None
        i = 0
        while give_card is None and i < len(self.cards_in_hand):
            card = self.cards_in_hand[i]
            if card.get_value() == value and card.get_color() == color:
                give_card = card
        if give_card is not None:
            self.cards_in_hand.remove(give_card)
        return give_card

    def ask_preferred_card(self) -> (int, Color):
        return 15, Color.Black

    def add_card(self, card: Card):
        self.cards_in_hand.append(card)
