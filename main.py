#!/usr/bin/env python3

from agents.basic_agent import BasicAgent
from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        BasicAgent(),
        RandomAgent(),
        RandomAgent(),
    ])

    # Start the game
    game.play(1000, 10)
