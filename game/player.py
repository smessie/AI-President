from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import Card


class Player:
    _player_id: int = 0

    def __init__(self):
        self.hand: List[Card] = []
        self.passed: bool = False
        self.player_id: int = Player._player_id
        self.position: Optional[int] = None
        Player._player_id += 1
