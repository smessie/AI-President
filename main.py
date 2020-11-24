#!/usr/bin/env python3

from agents.basic_agent import BasicAgent
from agents.dql_agent import DQLAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        DQLAgent('data/training/cp.ckpt', buffer_capacity=2000, hidden_layers=[100, 300], load_checkpoint=True),
        *(BasicAgent() for _ in range(3))
    ])

    # Start the game
    game.play(1000, 10)
