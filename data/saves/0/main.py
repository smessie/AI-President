#!/usr/bin/env python3
import asyncio

from agents.basic_agent import BasicAgent
from agents.dql_agent import DQLAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(
            DQLAgent(
                buffer_capacity=2000,
                hidden_layers=[78, 260],
                load_checkpoint=False, batch_size=50
            ) for _ in range(1)
        ),
        *(BasicAgent() for _ in range(3))
    ])

    # Start the game
    asyncio.run(game.play(500, 20))
