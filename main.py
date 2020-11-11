#!/usr/bin/env python3

from game.president import President
from agents.basic_agent import BasicAgent
from agents.simple_agent import SimpleAgent
from agents.random_agent import RandomAgent

if __name__ == "__main__":
    game = President([
        BasicAgent(),
        RandomAgent(),
        RandomAgent(),
    ])

    # Start the game
    game.play(1000, 10)
