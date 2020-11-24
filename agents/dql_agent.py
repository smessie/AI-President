from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Any, List, Optional, Union

from ai.model import PresidentModel
from ai.representation_mapper import map_cards_to_vector, map_action_to_cards
from game.agent import Agent
from game.player import Player
from game.table import Table

if TYPE_CHECKING:
    from game.card import Card


class DQLAgent(Agent):
    def __init__(
            self,
            filepath: str,
            buffer_capacity: int = 1000,
            hidden_layers: List[int] = [64],
            load_checkpoint: bool = False,
            gamma: float = 0.9,
            batch_size: int = 100,
    ):
        super().__init__(Player())
        self.model: PresidentModel = PresidentModel(
            hidden_layers=hidden_layers,
            gamma=gamma,
            sample_batch_size=batch_size
        )
        self.temp_memory: List[Union[List[int], int, int, Optional[List[int]]]] = []
        self.replay_buffer: List[Union[List[int], int, int, Optional[List[int]]]] = []
        self.replay_buffer_capacity = buffer_capacity
        self.filepath = filepath

        if load_checkpoint:
            self.model.load(filepath)

    def make_move(self, table: Table) -> None:
        """
        Agent makes a move by using Deep Q-Learning.
        """
        cards_in_hand_vector: List[int] = map_cards_to_vector(self.player.hand)
        cards_previous_move_vector: List[int] = map_cards_to_vector(table.last_move()[0] if table.last_move() else [])
        all_played_cards_vector: List[int] = map_cards_to_vector(
            list(chain.from_iterable([*map(lambda x: x[0], table.played_cards), *table.discard_pile])))

        input_vector = cards_in_hand_vector + cards_previous_move_vector + all_played_cards_vector

        if self.temp_memory:  # Set next state of previous move
            self.temp_memory[-1][3] = input_vector

        calculated_move: int = self.model.calculate_next_move(input_vector)

        self.temp_memory.append([
            input_vector,
            calculated_move,
            0,
            None
        ])

        move: Optional[List[Card]] = map_action_to_cards(calculated_move, self.player.hand)

        if move is None:
            move = []  # TODO illegal move, do we wat to handle this this way?
            # punish at the end? => -0.01 from final reward per illegal move
            # Save move to memory when illegal-> with negative reward in already existing self.temp_memory[-1]?

        table.try_move(self, move)

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)

    def game_end_callback(self, agent_finish_order: List[Agent], table: Table):
        """
        The game has ended, Train the model based on the moves made during the game and before the game.
        """
        reward = len(agent_finish_order) - list(map(
            lambda agent: agent.player.player_id, agent_finish_order
        )).index(self.player.player_id)
        # add reward to moves of last round.
        for move in self.temp_memory:
            new_move: Any = list(move)
            new_move[2] = reward
            self.replay_buffer.append(new_move)
            if len(self.replay_buffer) > self.replay_buffer_capacity:
                self.replay_buffer.pop(0)
        self.temp_memory.clear()

        self.model.train_model(self.replay_buffer)
        self.model.save(self.filepath)
