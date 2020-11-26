#!/usr/bin/env python3

from agents.basic_agent import BasicAgent
from agents.dql_agent import DQLAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        DQLAgent('data/training/cp.ckpt', buffer_capacity=2000, hidden_layers=[100, 300], load_checkpoint=False),
        *(BasicAgent() for _ in range(3))
    ])  # TODO: tegen random agent

    # Start the game
    game.play(1000, 10)
