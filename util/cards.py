from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from game.card import Card


def get_played_value(cards: List[Card]) -> Optional[int]:
    """
    Get the value of a stack off cards if they are all the same except for some 2s, -1 if not and None if only 2s
    """
    played_value: Optional[int] = None
    for card in cards:
        if card.value != 15:  # A 2-card has value 15.
            if played_value and played_value != card.value:
                # Cards do not have the same rank
                return -1
            played_value = card.value
    return played_value


def print_cards(cards: List[Card]) -> None:
    card_strings = ['' for _ in range(7)]
    for card in cards:
        for i, line in enumerate(card.get_card_strings_stripped()):
            card_strings[i] += line
    for line in card_strings:
        print(line)


def print_cards_string(cards: List[Card]) -> str:
    result = ''
    card_strings = ['' for _ in range(5)]
    for card in cards:
        for i, line in enumerate(card.get_card_strings_stripped()):
            card_strings[i] += line
    for line in card_strings:
        result += line + '\n'
    return result
