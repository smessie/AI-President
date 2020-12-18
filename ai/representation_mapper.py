from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from game.card import Card


def map_cards_to_vector(cards: List[Card]) -> List[int]:
    """
    Map a list of cards to an input vector for our neural network.
    """
    vector: List[int] = [0 for _ in range(13)]
    for card in cards:
        # Values of cards start at 3 instead of 0. To start indexing from 0 subtract 3 from the value.
        vector[card.get_value() - 3] += 1
    return vector


def map_vector_to_cards(vector: List[int], hand: List[Card]) -> Optional[List[Card]]:
    """
    Map an output vector to a list of cards for our neural network.
    """
    cards: List[Card] = []
    for value, amount in enumerate(vector):
        for _ in range(amount):
            i: int = 0
            matched_card: Optional[Card] = None
            while i < len(hand) and not matched_card:
                if hand[i].get_value() == (value + 3) and hand[i] not in cards:
                    matched_card = hand[i]
                i += 1
            if matched_card:
                cards.append(matched_card)
            else:
                return None
    return cards


def map_action_to_cards(action: int, hand: List[Card]) -> Optional[List[Card]]:
    if action == 240:
        return []
    assert 0 <= action <= 239, 'action should be between 0 and 239'

    amount_of_twos: int = action // 48
    amount_of_specific_cards: int = ((action % 48) // 12) + 1
    card_value: int = action % 12
    vector = [0 if i != card_value else amount_of_specific_cards for i in range(12)] + [amount_of_twos]
    return map_vector_to_cards(vector, hand)


def map_cards_to_action(cards: List[Card]) -> int:
    vector: List[int] = map_cards_to_vector(cards)
    amount_of_twos: int = vector[-1]
    amount_of_specific_cards: int = 0
    card_value: int = -1
    for value, amount in enumerate(vector[:-1]):
        if amount != 0:
            assert card_value == -1, 'cannot map illegal move to action'
            card_value = value
            amount_of_specific_cards = amount
    if card_value == -1:
        assert amount_of_twos == 0, 'cannot map only twos to action'
        return 240  # pass
    action: int = (amount_of_specific_cards - 1) * 12 + amount_of_twos * 48 + card_value
    return action
