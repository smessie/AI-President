import enum
import random


class Color(enum.Enum):
    Black = 1
    Red = 2


class Suit(enum.Enum):
    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4


class Card:
    """"A card in the deck"""

    def __init__(self, value: int, color: Color, suit: Suit, name: str):
        self.value = value
        self.color = color
        self.suit = suit
        self.name = name

    def get_value(self) -> int:
        return self.value

    def get_color(self) -> Color:
        return self.color

    def get_suit(self) -> Suit:
        return self.suit

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.value == other.value and self.color == other.color

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.value < other.value or (self.value == other.value and self.color < other.color)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.value > other.value or (self.value == other.value and self.color > other.value)

    def __ge__(self, other):
        return self > other or self == other


def initial_deck_cards():
    cards = []
    values = [(3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "Jack"),
              (12, "Queen"), (13, "King"), (14, "Ace"), (15, "2")]
    for value in values:
        for color in Color:
            for suit in Suit:
                cards.append(Card(value[0], color, suit, color.name + " " + values[1] + " of " + suit))
    random.shuffle(cards)
    return cards
