from typing import List, Tuple

import tensorflow as tf
import numpy as np


class PresidentModel:

    def __init__(self, hidden_layers: List[int]):
        assert len(hidden_layers) > 0, 'At least one hidden layer required'
        self._model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=hidden_layers[0], activation='relu', input_dim=13 * 3),
            *(tf.keras.layers.Dense(units=units, activation='relu') for units in hidden_layers[1:]),
            tf.keras.layers.Dense(units=13, activation='softmax'),  # TODO geen activation
        ])
        self._model.summary()
        self._model.compile(
            loss=tf.keras.losses.MeanSquaredError(),
            optimizer=tf.keras.optimizers.SGD(),
            metrics=[tf.keras.metrics.MeanSquaredError()],
        )

    def calculate_next_move(self, cards_in_hand_vector, cards_previous_move_vector, all_played_cards_vector) -> List[float]:
        input_data = np.array(cards_in_hand_vector + cards_previous_move_vector + all_played_cards_vector)[np.newaxis, :]
        prediction = self._model.predict(input_data)
        return prediction[0].tolist()

    def train_model(self, data: List[Tuple[List[int], List[float], int]]):
        input_data: List[List[int]] = [*map(lambda x: x[0], data)]
        output_data: List[List[int]] = [*map(lambda x: x[1], data)]
        # TODO: how to pass reward to network?
        self._model.fit(x=input_data, y=output_data, batch_size=len(input_data), epochs=10, verbose=0)
        # TODO: use train_on_batch
        pass
