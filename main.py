import game.president as President
import game.player as Player

if __name__ == "__main__":
    game = President.President()

    # Let players join the game
    game.add_player(Player.Player(game))

    # Start the game when we're done adding players
    game.start_game(amount_of_rounds=1)
