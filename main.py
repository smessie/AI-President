from game.president import President
from agents.basic_agent import BasicAgent
from agents.simple_agent import SimpleAgent

if __name__ == "__main__":
    game = President([
        BasicAgent(),
        *(SimpleAgent() for _ in range(3))
    ])

    # Start the game
    game.play(1000, 10)
