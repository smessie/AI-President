from typing import List, Union, Optional

import numpy as np
import tensorflow as tf
import random


class PresidentModel:

    def __init__(self, hidden_layers: List[int], gamma: float = 0.9, sample_batch_size: int = 32):
        assert len(hidden_layers) > 0, 'At least one hidden layer required'
        self._model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=hidden_layers[0], activation='relu', input_dim=13 * 3),
            *(tf.keras.layers.Dense(units=units, activation='relu') for units in hidden_layers[1:]),
            tf.keras.layers.Dense(units=20*12+1),
        ])
        self._model.summary()
        self._model.compile(
            loss=tf.keras.losses.MeanSquaredError(),
            optimizer=tf.keras.optimizers.SGD(),
            metrics=[tf.keras.metrics.MeanSquaredError()],
        )
        self._gamma = gamma
        self._sample_batch_size = sample_batch_size

    def calculate_next_move(self, data: List[int])\
            -> int:
        input_data = \
            np.array(data)[np.newaxis, :]
        prediction = self._model.predict(input_data)
        return np.argmax(prediction[0])

    def train_model(self, data: List[Union[List[int], int, int, Optional[List[int]]]]):
        #input_data: List[List[int]] = [*map(lambda x: x[0], data)]
        #output_data: List[List[int]] = [*map(lambda x: x[1], data)]
        # TODO: how to pass reward to network?
        #self._model.fit(x=input_data, y=output_data, batch_size=len(input_data), epochs=10, verbose=0)
        # TODO: use train_on_batch

        sample_batch = random.sample(data, self._sample_batch_size) if self._sample_batch_size < len(data) else data
        for state, action, reward, next_state in sample_batch:

            target = reward
            if next_state:
                ns_np = np.array(next_state).reshape(-1, 39)
                target = reward + self._gamma * np.amax(self._model.predict(ns_np)[0])

            state_np = np.array(state).reshape(-1, 39)
            target_f = self._model.predict(state_np)
            target_f[0][action] = target
            self._model.train_on_batch(state_np, target_f)

    def save(self, filepath: str):
        # tf.keras.callbacks.ModelCheckpoint(filepath=filepath, save_weights_only=True, verbose=1)
        self._model.save_weights(filepath, overwrite=True)

    def load(self, filepath: str):
        self._model.load_weights(filepath)
