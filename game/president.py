from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Optional, Tuple

from tqdm import tqdm

from game.table import Table
from util.cards import get_played_value
from util.iterator import CustomIterator

if TYPE_CHECKING:
    from game.agent import Agent
    from game.card import Card


class President:
    """
    A class containing the game logic.
    """

    def __init__(self, agents: List[Agent]):
        self.agents: List[Agent] = agents
        self.passed_agents: Dict[Agent, bool] = {
            agent: False for agent in self.agents
        }
        self.agent_finish_order: List[Agent] = []
        self.agent_iterator: CustomIterator = CustomIterator(agents)
        self.table = Table(self)

    def play(self, games: int, rounds: int) -> None:
        """
        Start the game. Play a certain amount of games each consisting of a certain amount of rounds.
        """
        progress = tqdm(total=games * rounds)

        for g in range(games):
            for r in range(rounds):
                # Update the progress bar
                progress.set_description(
                    f"Running round {r} of game {g}. "
                    f"Last winner: {self.agent_finish_order[0].player.player_id if self.agent_finish_order else None}")
                progress.update()

                # Reset from the previous round
                self._reset()

                # If this is not the first round exchange cards
                if r != 0:
                    self._exchange_cards()
                self.agent_finish_order = []

                # Play the round
                for agent in self._get_play_order():
                    agent.make_move(self.table)

                    # If the player finished this round award it by giving it its position.
                    if len(agent.player.hand) == 0:
                        self.agent_finish_order.append(agent)

                for agent in self.agents:
                    agent.game_end_callback(self.agent_finish_order, self.table)

        progress.close()

    def on_move(self, agent: Agent, cards: List[Card]) -> Tuple[int, bool]:
        """
        Handle move from Agent, We can be sure the agent can actually play the card.
        return (reward, is_final).
        """
        if not cards:
            # A Pass, disable the player for this round
            self.passed_agents[agent] = True
            #print('Player passed')
            return -5, False  # TODO fix reward

        # A pass is a valid move.
        if len(cards) != 0:
            # WARNING: when playing with 2 decks of cards this is not sufficient.
            if not all(card in agent.player.hand for card in cards):
                self.passed_agents[agent] = True
                #print('Player can\'t make move')
                return -10, False

        # Previous value should be lower
        if self.valid_move(cards, debug=False):
            #print('OK')
            self.table.do_move(agent, cards)
            return 10, False  # TODO fix reward
        else:
            self.passed_agents[agent] = True
            return -10, False  # TODO fix reward

    def valid_move(self, cards: List[Card], debug=False) -> bool:


        last_move: Tuple[List[Card], Agent] = self.table.last_move()

        # If multiple cards are played length should be at least the same.
        if cards and last_move and len(cards) < len(last_move[0]):
            if debug:
                print('Not enough cards')
            return False

        # Check that each played card in the trick has the same rank, or if not, it is a 2.
        played_value: Optional[int] = get_played_value(cards)
        if not played_value or played_value < 0:
            if debug:
                print('value too low')
            return False
        last_move_value: int = get_played_value(last_move[0]) if last_move else None

        # Previous value should be lower
        return not last_move or last_move_value <= played_value

    def _reset(self) -> None:
        """
        - (Re)divide cards
        - reset the finish order
        - reset the playing table
        """
        for i, hand in enumerate(self.table.divide(len(self.agents))):
            self.agents[i].player.hand = hand
        self.table.reset()

    def _exchange_cards(self) -> None:
        # Todo discuss this, but for now only the first and last player trade cards
        first: Agent = self.agent_finish_order[0]
        last: Agent = self.agent_finish_order[-1]
        preferred_cards: List[Card] = first.get_preferred_card_order(self.table)

        # Hand best card from loser to winner
        card_index = 0
        while preferred_cards[card_index] not in last.player.hand:
            card_index += 1

        exchange_card: Card = last.player.hand[card_index]
        first.player.hand.append(exchange_card)
        last.player.hand.remove(exchange_card)

        # Hand lowest card from winner to loser
        exchange_card = sorted(first.player.hand)[0]
        first.player.hand.remove(exchange_card)
        last.player.hand.append(exchange_card)

    def _get_play_order(self) -> Iterator[Agent]:
        """
        Return the player order, this is an iterator so this allows for cleaner code in the President class.
        """
        # As long as there are 2 unfinished players
        while [len(agent.player.hand) > 0 for agent in self.agents].count(True) >= 2:
            self.agent_iterator.next()
            nr_skips: int = 0

            while nr_skips <= len(self.agents) and (
                    len(self.agent_iterator.get().player.hand) == 0 or self.passed_agents[self.agent_iterator.get()]):
                self.agent_iterator.next()
                nr_skips += 1

            if nr_skips > len(self.agents):
                # All agents have no cards left
                if all(len(agent.player.hand) == 0 for agent in self.agents):
                    return
                # Some player still has a card. Start a new trick
                # The check is needed for if a player makes an invalid move
                last_agent = self.table.last_move()[1] if self.table.last_move() else self.agent_iterator.get()

                self.table.new_trick()
                self.passed_agents = {
                    agent: False for agent in self.agents
                }

                # The player that has made the last move can start in the new trick
                while self.agent_iterator.get() != last_agent:
                    self.agent_iterator.next()
                # We found the player, but the loop will call next, so we have to call previous to neutralize this.
                self.agent_iterator.previous()
                continue

            yield self.agent_iterator.get()
        # The unfinished player comes last, add it to the last_played lis
        self.agent_finish_order.append(list(filter(lambda x: len(x.player.hand) > 0, self.agents))[0])
