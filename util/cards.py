from __future__ import annotations

import re
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


def match_move(input_move: str, possible_moves: List[List[Card]]) -> Optional[List[Card]]:
    if input_move == "0" and [] in possible_moves:
        return []
    input_move = input_move.upper()
    if re.match('^[02-9XJQKA]+$', input_move) is None:
        return None
    cards = list(input_move)
    size = len(cards)
    for move in possible_moves:
        matching_cards = cards[:]
        if size == len(move):
            skip = False
            for card in move:
                char_value: str = card.get_char_value()
                if char_value in matching_cards:
                    matching_cards.remove(char_value)
                else:
                    skip = True
                    break
            if not skip:
                return move
    return None


def print_cards(cards: List[Card]) -> None:
    card_strings = ['' for _ in range(7)]
    for card in cards:
        for i, line in enumerate(card.get_card_strings()):
            card_strings[i] += line
    for line in card_strings:
        print(line)


def print_cards_string(cards: List[Card]) -> str:
    result = '```\n'
    card_strings = ['' for _ in range(5)]
    for card in cards:
        for i, line in enumerate(card.get_card_strings_stripped()):
            card_strings[i] += line
    for line in card_strings:
        result += line + '\n'
    result += '```\n'
    return result
