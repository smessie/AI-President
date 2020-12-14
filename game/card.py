import enum
from typing import List


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

    def get_symbol(self) -> str:
        return ['', '♣', '♦', '♠', '♥'][self.value]


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
        return self.value < other.value or \
            (self.value == other.value and self.suit.get_color() < other.suit.get_color())

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.value > other.value or \
            (self.value == other.value and self.suit.get_color() > other.suit.get_color())

    def __ge__(self, other):
        return self > other or self == other

    def __hash__(self):
        return hash(self.suit.get_color()) + hash(self.value)

    def __repr__(self):
        return self.name

    def get_card_strings(self) -> List[str]:
        value = self.value if self.value < 10 else (
            'X' if self.value == 10 else (
                'J' if self.value == 11 else (
                    'Q' if self.value == 12 else (
                        'K' if self.value == 13 else (
                            'A' if self.value == 14 else '2'
                        )
                    )
                )
            )
        )
        return [
            "┌---------┐",
            f"| {value}       |",
            "|         |",
            f"|    {self.suit.get_symbol()}    |",
            "|         |",
            f"|       {value} |",
            "└---------┘",
        ]

    def get_card_strings_stripped(self) -> List[str]:
        value = self.value if self.value < 10 else (
            'X' if self.value == 10 else (
                'J' if self.value == 11 else (
                    'Q' if self.value == 12 else (
                        'K' if self.value == 13 else (
                            'A' if self.value == 14 else '2'
                        )
                    )
                )
            )
        )
        return [
            "┌-----┐ ",
            f"  |  {value}       |  ",
            f"  |   {self.suit.get_symbol()}  |  ",
            f"  |       {value}  |  ",
            "└-----┘ ",
        ]
