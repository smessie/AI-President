from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from game.card import Card


def get_played_value(cards: List[Card]) -> Optional[int]:
    """
    Get the value of a stack off cards if they are all the same except for some 2s, -1 if not and None if only 2s
    """
    played_value: Optional[int] = None
    for card in cards:
        if card.value != 2:
            if played_value and played_value != card.value:
                # Cards do not have the same rank
                return -1
            played_value = card.value
    return played_value
