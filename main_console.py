#!/usr/bin/env python3

from agents.basic_agent import BasicAgent
from agents.console_agent import ConsoleAgent
from agents.dql_agent import DQLAgent
from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(
            DQLAgent(
                buffer_capacity=2000,
                hidden_layers=[78, 260],
                load_checkpoint=True,  # Required for playing against trained agent if training is now disabled!
                batch_size=50,
                epsilon=0,  # Ignored when training is disabled
                lower_eps_over_time=0,  # Ignored when training is disabled
                track_training_loss=True,
                living_reward=0,  # Ignored when training is disabled
                training_mode=False,  # Marks that we are no longer training
                filepath="data/saves/15/training-0/cp.ckpt",
                csv_filepath="data/saves/15/results/wins-benchmark.csv"
            ) for _ in range(0)
        ),
        *(ConsoleAgent(input('Enter your name:')) for _ in range(1)),
        *(RandomAgent(f'Randy {i+1}') for i in range(2)),
        *(BasicAgent(f'Basy {i+1}') for i in range(1))
    ])

    # Start the game
    await game.play(250, 20)
