from game.president import President
from agents.simple_agent import SimpleAgent

if __name__ == "__main__":
    game = President([
        SimpleAgent() for _ in range(3)
    ])

    # Start the game
    game.play(1000, 10)
