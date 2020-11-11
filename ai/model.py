from typing import List

import tensorflow as tf


class PresidentModel:

    def __init__(self, hidden_layers: List[int]):
        assert len(hidden_layers) > 0, 'At least one hidden layer required'
        self._model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=hidden_layers[0], activation='relu', input_dim=13 * 3),
            *(tf.keras.layers.Dense(units=units, activation='relu') for units in hidden_layers[1:]),
            tf.keras.layers.Dense(units=13, activation='softmax'),
        ])
        self._model.summary()
        self._model.compile(
            loss=tf.keras.losses.MeanSquaredError(),
            optimizer=tf.keras.optimizers.SGD(),
            metrics=[tf.keras.metrics.MeanSquaredError()],
        )

    def calculate_next_move(self, cards_in_hand_vector, cards_previous_move_vector, all_played_cards_vector):
        pass

