import game.Deck as Deck
import game.Player as Player
import itertools
import random
from typing import List, Dict


class President:
    def __init__(self, players: List[Player] = None):
        self.deck = Deck.Deck()
        self.players: List[Player] = players if players else []
        self.players_in_trick: List[Player] = []
        self.winning_round_order: List[Player] = []
        self.points: Dict[Player, int] = {}
        self.trick_starter: Player = None

    def add_player(self, player: Player):
        """"Add a new player to the game"""
        self.players.append(player)

    def start_game(self, amount_of_rounds: int = 5):
        """A series of rounds."""
        self.check_enough_players()
        self.setup_points()
        for _ in range(amount_of_rounds):
            self.divide_cards()
            self.start_new_round()
            self.collect_remaining_cards()

    def start_new_round(self):
        """Each round ends with a winner, the President"""
        self.exchange_cards_presidents_losers()
        self.trick_starter = self.winning_round_order[0] if self.winning_round_order else self.players[0]
        self.winning_round_order.clear()
        while len(self.winning_round_order) + 1 < len(self.players):
            self.start_new_trick()
        self.assign_points()

    def start_new_trick(self):
        """A new trick starts with a clear deck and the player who played the highest cards in the previous trick may
        come out. A trick ends when everyone except 1 has passed."""
        # New trick, so add all players to it
        self.players_in_trick = [player for player in self.players if player not in self.winning_round_order]

        players_iterator = itertools.cycle(self.players)

        # Make sure the right player has to start
        for _ in range(self.players_in_trick.index(self.trick_starter)):
            next(players_iterator)

        while len(self.players_in_trick) >= 1:
            player = next(players_iterator)
            if player in self.players_in_trick:
                move = player.move(self.deck)
                if len(move) == 0:
                    # Player passed
                    self.players_in_trick.remove(player)
                elif not self.deck.is_valid_play(move):
                    # Player did invalid play
                    # Currently an assert, if changed later, make sure his cards aren't lost.
                    assert "Invalid play submitted by player."
                # Handle valid player move
                self.deck.played_cards.extend(move)
        self.deck.card_stack.extend(self.deck.played_cards)

    def exchange_cards_presidents_losers(self):
        if len(self.winning_round_order) == 0:
            return
        president = self.winning_round_order[0]
        loser = self.winning_round_order[-1]
        president_gives_card = president.give_worst_card()
        loser_gives_card = None
        while loser_gives_card is None:
            loser_gives_card = loser.give_specif_card(president.ask_preferred_card())
        president.add_card(loser_gives_card)
        loser.add_card(president_gives_card)

    def check_enough_players(self):
        assert len(self.players) >= 3, "Not enough players to start a game."

    def divide_cards(self):
        assert len(self.deck.card_stack) == 52, "Incomplete card stack."
        random.shuffle(self.deck.card_stack)
        players_iterator = itertools.cycle(self.players)
        while self.deck.card_stack:
            card = self.deck.card_stack.pop()
            next(players_iterator).add_card(card)

    def check_players_finished(self):
        for player in self.players:
            if player not in self.winning_round_order and not player.cards_in_hand:
                self.winning_round_order.append(player)
                if player in self.players_in_trick:
                    self.players_in_trick.remove(player)

    def collect_remaining_cards(self):
        for player in self.players:
            self.deck.card_stack.extend(player.cards_in_hand)
            player.cards_in_hand.clear()
        self.deck.card_stack.extend(self.deck.played_cards)
        self.deck.played_cards.clear()

    def setup_points(self):
        for player in self.players:
            self.points[player] = 0

    def assign_points(self):
        """Assign points based on the position in the winning_round_order list. To be adjusted."""
        self.points[self.winning_round_order[0]] += 2
        bonus = round((len(self.winning_round_order) / 2) / 10, 1)
        for i in range(1, len(self.winning_round_order)):
            self.points[self.winning_round_order[i]] += bonus
            bonus -= 0.1
