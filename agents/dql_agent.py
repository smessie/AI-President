from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Any, List, Optional, Union

from ai.model import PresidentModel
from ai.representation_mapper import map_action_to_cards, map_cards_to_vector
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
        # input vector (= cards in hand, previous move, all played cards); calculated move; reward; next move
        self.replay_buffer: List[Union[List[int], int, int, Optional[List[int]]]] = []
        self.replay_buffer_capacity: int = buffer_capacity
        self.filepath: str = filepath
        self.rounds_positions: Optional[List[int]] = None

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

        # TODO: implement epsilon greedy policy to take random *possible* moves
        calculated_move: int = self.model.calculate_next_move(input_vector)
        move: Optional[List[Card]] = map_action_to_cards(calculated_move, self.player.hand)

        if move is None:
            move = []

        table.try_move(self, move)

    def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        """
        The game has ended, Train the model based on the moves made during the game and before the game.
        """
        reward_list = list(map(lambda agent: agent.player.player_id, agent_finish_order))
        # add reward to moves of last round.
        for agent in table.game.temp_memory:
            for move in table.game.temp_memory[agent]:
                new_move: Any = list(move)
                if new_move[2] == 0:
                    # If we didn't set a negative reward already, set the reward equal to the given reward for the game.
                    new_move[2] = len(agent_finish_order) - reward_list.index(agent.player.player_id)
                self.replay_buffer.append(new_move)
                if len(self.replay_buffer) > self.replay_buffer_capacity:
                    self.replay_buffer.pop(0)
        table.game.reset_temp_memory()

        self.model.train_model(self.replay_buffer)

        if not self.rounds_positions:
            self.rounds_positions = [0 for _ in range(len(agent_finish_order))]

        self.rounds_positions[agent_finish_order.index(self)] += 1

    def game_end_callback(self, game_nr: int):
        self.model.save(self.filepath)

        with open('data/results/wins.csv', 'a+') as file:
            file.write(f'{game_nr},{",".join(map(str, self.rounds_positions))}\n')

        self.rounds_positions = None
