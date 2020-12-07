#!/usr/bin/env python3

from agents.basic_agent import BasicAgent
from agents.dql_agent import DQLAgent
from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(
            DQLAgent(
                buffer_capacity=2000,
                hidden_layers=[78, 260],
                load_checkpoint=False,
                batch_size=50,
                epsilon=20,
                track_training_loss=True
            ) for _ in range(1)
        ),
        *(RandomAgent() for _ in range(3))
    ])

    # Start the game
    game.play(250, 20)
