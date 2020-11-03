from typing import List

from game.card import Card
from game.deck import Deck
from game.president import President


class Player:
    _player_id = 0

    def __init__(self):
        self.hand: List[Card] = []
        self.player_id = Player._player_id
        self.position = None
        Player._player_id += 1
