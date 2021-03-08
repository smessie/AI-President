#!/usr/bin/env python3

from agents.better_agent import BetterAgent
from agents.discord_agent import DiscordAgent
from agents.dql_agent import DQLAgent
from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(
            DQLAgent(
                buffer_capacity=2000,
                hidden_layers=[78, 260],
                load_checkpoint=True,
                batch_size=100,
                epsilon=5,
                lower_eps_over_time=0,
                track_training_loss=True,
                living_reward=-0.1,
                training_mode=False,
                filepath="data/saves/10/training-0/cp.ckpt",
                csv_filepath="data/saves/10/results/wins-benchmark.csv"
            ) for _ in range(1)
        ),
        *(DiscordAgent() for _ in range(1)),
        *(RandomAgent(f'Randy {i + 1}') for i in range(1)),
        *(BetterAgent(f'Betty {i + 1}') for i in range(1))
    ])

    # Start the game
    game.play(250, 20, 0)
