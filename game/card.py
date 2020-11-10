import enum


class Color(enum.Enum):
    Black = 1
    Red = 2

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


class Suit(enum.Enum):
    Clubs = 1
    Diamonds = 2
    Spades = 3
    Hearts = 4

    def get_color(self):
        """Suits have fixed colors"""
        return Color.Red if self.value % 2 == 0 else Color.Black


class Card:
    """"A card in the deck"""

    def __init__(self, value: int, suit: Suit, name: str):
        self.value = value
        self.suit = suit
        self.name = name

    def get_value(self) -> int:
        return self.value

    def get_color(self) -> Color:
        return self.suit.get_color()

    def get_suit(self) -> Suit:
        return self.suit

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.value == other.value and self.suit.get_color() == other.suit.get_color()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.value < other.value or (
                self.value == other.value and self.suit.get_color() < other.suit.get_color())

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.value > other.value or (
                self.value == other.value and self.suit.get_color() > other.suit.get_color())

    def __ge__(self, other):
        return self > other or self == other
