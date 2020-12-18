import random
from os import mkdir, path
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import tensorflow as tf


class PresidentModel:

    def __init__(
            self,
            hidden_layers: List[int],
            gamma: float = 0.9,
            sample_batch_size: int = 32,
            track_training_loss: bool = False,
            filepath: str = None,
            early_stopping: bool = False,
            optimizer=None,
            loss=None,
            metrics=None,
    ):
        if optimizer is None:
            optimizer = tf.keras.optimizers.SGD()
        if loss is None:
            loss = tf.keras.losses.MeanSquaredError()
        if metrics is None:
            metrics = [tf.keras.metrics.MeanSquaredError()]

        assert len(hidden_layers) > 0, 'At least one hidden layer required'
        self._model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=hidden_layers[0], activation='relu', input_dim=13 * 3),
            *(tf.keras.layers.Dense(units=units, activation='relu') for units in hidden_layers[1:]),
            tf.keras.layers.Dense(units=20 * 12 + 1),
        ])
        self._model.summary()
        self._model.compile(
            loss=loss,
            optimizer=optimizer,
            metrics=metrics,
        )
        self._gamma = gamma
        self._sample_batch_size = sample_batch_size
        self._track_training_loss = track_training_loss
        self.filepath = filepath if filepath else 'data/results/training_loss.csv'
        self.early_stopping = early_stopping

        if track_training_loss:
            for p in [Path(self.filepath)]:
                if not path.exists(p.parent.__str__()):
                    mkdir(p.parent)

    def calculate_next_move(self, data: List[int]) \
            -> List[int]:
        input_data = \
            np.array(data)[np.newaxis, :]
        prediction = self._model.predict(input_data)
        return prediction[0]

    def train_model(self, data: List[Union[List[int], int, int, Optional[List[int]]]]) -> bool:
        sample_batch = random.sample(data, self._sample_batch_size) if self._sample_batch_size < len(data) else data
        states = []
        targets = []

        for state, action, reward, next_state in sample_batch:

            target = reward
            if next_state is not None:
                target = reward + self._gamma * np.amax(self._model.predict(next_state)[0])

            target_f = self._model.predict(state)
            target_f[0][action] = target
            states.append(state[0])
            targets.append(target_f[0])

        training_loss = self._model.train_on_batch(np.array(states), np.array(targets))
        if self._track_training_loss:
            # Log training loss values in file to check if they decrease and they are different from infinity/NaN
            with open(self.filepath, 'a+') as file:
                file.write(f'{",".join(map(str, training_loss))}\n')
        if self.early_stopping:
            if training_loss[0] > 1000:
                return True
        return False

    def save(self, filepath: str):
        # tf.keras.callbacks.ModelCheckpoint(filepath=filepath, save_weights_only=True, verbose=1)
        self._model.save_weights(filepath, overwrite=True)

    def load(self, filepath: str):
        self._model.load_weights(filepath)
