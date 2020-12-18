#!/usr/bin/env python3

import tensorflow as tf

from agents.basic_agent import BasicAgent
from agents.console_agent import ConsoleAgent
from agents.dql_agent import DQLAgent
from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(
            DQLAgent(
                buffer_capacity=500,
                hidden_layers=[78, 260],
                load_checkpoint=False,
                batch_size=50,
                epsilon=20,
                lower_eps_over_time=0,
                track_training_loss=True,
                living_reward=-0.01,
                training_mode=True,
                gamma=0.9,
                early_stopping=False,
            ) for _ in range(1)
        ),
        *(RandomAgent() for _ in range(1)),
        *(BasicAgent() for _ in range(2)),
        #ConsoleAgent()
    ])

    # Start the game
    game.play(250, 20)