from __future__ import annotations

from itertools import chain
from os import mkdir, path
from pathlib import Path
from random import choice, randint
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union

from ai.model import PresidentModel
from ai.representation_mapper import map_action_to_cards, map_cards_to_vector
from game.agent import Agent
from game.player import Player
from game.table import Table

if TYPE_CHECKING:
    from game.card import Card


class DQLAgent(Agent):
    """
    lower_eps_over_time adjusts the epsilon greedy policy by lowering epsilon over time.
    Every round, the eps_over_time is decreased with one, eps_over_time/lower_eps_over_time is used as epsilon in the
     epsilon greedy policy to do exploration as long as eps_over_time is bigger than zero.

    In training_mode=False, the epsilon parameter is ignored and all moves are requested from the model.
    In this mode there is no learning, no data is written to the model.
    """

    def __init__(
            self,
            filepath: str = None,
            csv_filepath: str = None,
            buffer_capacity: int = 1000,
            hidden_layers: List[int] = [64],
            load_checkpoint: bool = False,
            gamma: float = 0.9,
            batch_size: int = 100,
            epsilon: int = 5,
            lower_eps_over_time: int = 0,
            start_eps_over_time: int = 100,
            track_training_loss: bool = False,
            living_reward: float = -0.01,
            training_mode: bool = True,
            early_stopping: bool = False,
            optimizer=None,
            loss=None,
            metrics=None,
            player_name: str = None,
    ):
        super().__init__(Player(player_name if player_name is not None else 'DQLAgent'))
        print(f'Player {self.player.get_player_id()} is {hidden_layers},{buffer_capacity}')
        self.model: PresidentModel = PresidentModel(
            hidden_layers=hidden_layers,
            gamma=gamma,
            sample_batch_size=batch_size,
            track_training_loss=track_training_loss,
            filepath=f'data/results/training_loss-{self.player.get_player_id()}.csv',
            early_stopping=early_stopping,
            optimizer=optimizer,
            loss=loss,
            metrics=metrics
        )
        # input vector (= cards in hand, previous move, all played cards); calculated move; reward; next move
        self.replay_buffer: List[Union[List[int], int, int, Optional[List[int]]]] = []
        self.replay_buffer_capacity: int = buffer_capacity
        self.filepath: str = filepath if filepath else f'data/training-{self.player.player_id}/cp.ckpt'
        self.csv_filepath: str = csv_filepath if csv_filepath else f'data/results/wins-{self.player.player_id}.csv'
        self.epsilon: int = epsilon
        self.lower_eps_over_time: int = lower_eps_over_time
        self.start_eps_over_time: float = start_eps_over_time / 100
        self.eps_over_time: int = lower_eps_over_time
        self.living_reward: float = living_reward
        self.training_mode: bool = training_mode

        for p in [Path(self.filepath), Path(self.csv_filepath)]:
            if not path.exists(p.parent.__str__()):
                mkdir(p.parent)

        self.rounds_positions: Optional[List[int]] = None
        self.triggered_early_stopping = False

        if load_checkpoint:
            self.model.load(filepath)

    async def make_move(self, table: Table) -> None:
        """
        Agent makes a move by using Deep Q-Learning.
        """
        cards_in_hand_vector: List[int] = map_cards_to_vector(self.player.hand)
        cards_previous_move_vector: List[int] = map_cards_to_vector(table.last_move()[0] if table.last_move() else [])
        all_played_cards_vector: List[int] = map_cards_to_vector(
            list(chain.from_iterable([*map(lambda x: x[0], table.played_cards), *table.discard_pile])))

        input_vector = cards_in_hand_vector + cards_previous_move_vector + all_played_cards_vector

        rand: int = randint(0, 100)

        exploration_chance: float = self.epsilon
        if self.eps_over_time > 0:
            exploration_chance: float = (self.eps_over_time / self.lower_eps_over_time) * self.start_eps_over_time
        if not self.training_mode:
            exploration_chance = 0
        if rand >= exploration_chance:
            q_values: List[Tuple[int, int]] = sorted(
                [(i, v) for i, v in enumerate(self.model.calculate_next_move(input_vector))
                 ], key=lambda x: -x[1])

            i = 0
            move: Optional[List[Card]] = map_action_to_cards(q_values[i][0], self.player.hand)
            while i < len(q_values) and (move is None or not table.game.valid_move(move, self)):
                i += 1
                if i >= len(q_values):
                    move = []
                else:
                    move = map_action_to_cards(q_values[i][0], self.player.hand)

            table.try_move(self, move)
        else:
            table.try_move(self, choice(self.player.get_all_possible_moves(table, self)))

    async def get_preferred_card_order(self, table: Table) -> List[Card]:
        """
        Returns the preferred cards to exchange in the beginning of a round in descending value order.
        """
        possible_cards = list(set(table.deck.card_stack) - set(self.player.hand))
        return sorted(possible_cards, reverse=True)

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        """
        The game has ended, Train the model based on the moves made during the game and before the game.
        """
        if self.training_mode:
            reward_list = list(map(lambda agent: agent.player.player_id, agent_finish_order))
            # add reward to moves of last round.
            for agent in table.game.temp_memory:
                total_living_reward: float = \
                    len(table.game.temp_memory[agent]) * self.living_reward + self.living_reward
                for move in table.game.temp_memory[agent]:
                    new_move: Any = list(move)
                    if new_move[2] == 0:
                        # If we didn't set a negative reward already, set the reward equal to the given reward for the
                        # game.
                        new_move[2] = (len(agent_finish_order) -
                                       (reward_list.index(agent.player.player_id) - 1) ** 2) + total_living_reward
                    self.replay_buffer.append(new_move)
                    if len(self.replay_buffer) > self.replay_buffer_capacity:
                        self.replay_buffer.pop(0)
                    total_living_reward -= self.living_reward

            self.triggered_early_stopping = self.model.train_model(self.replay_buffer) or self.triggered_early_stopping
            self.model.save(self.filepath)

        if self.eps_over_time > 0:
            self.eps_over_time -= 1

        if not self.rounds_positions:
            self.rounds_positions = [0 for _ in range(len(agent_finish_order))]

        self.rounds_positions[agent_finish_order.index(self)] += 1

    async def game_end_callback(self, game_nr: int) -> bool:
        if self.training_mode:
            self.model.save(self.filepath)

        with open(self.csv_filepath, 'a+') as file:
            file.write(f'{game_nr},{",".join(map(str, self.rounds_positions))}\n')

        self.rounds_positions = None
        return self.triggered_early_stopping
