from __future__ import annotations

import asyncio
from itertools import chain
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional, Tuple, Union

import numpy as np
from tqdm import tqdm

from ai.representation_mapper import map_cards_to_action, map_cards_to_vector
from game.table import Table
from util.cards import get_played_value, print_cards
from util.iterator import CustomIterator

if TYPE_CHECKING:
    from game.agent import Agent
    from game.card import Card


class President:
    """
    A class containing the game logic.
    """

    def __init__(self, agents: List[Agent], verbose: bool = False):
        self.agents: List[Agent] = agents
        self.passed_agents: Dict[Agent, bool] = {
            agent: False for agent in self.agents
        }
        self.agent_finish_order: List[Agent] = []
        self.agent_iterator: CustomIterator = CustomIterator(agents)
        self.table = Table(self)
        self.scum = None

        # Dict[player/agent,
        # input vector (= cards in hand, previous move, all played cards); calculated move; reward; next move]
        self.temp_memory: Dict[Agent, List[Union[List[int], int, int, Optional[List[int]]]]] = {}
        for agent in agents:
            self.temp_memory[agent] = []
        self.verbose = verbose

    async def play(self, games: int, rounds: int, start_at_game: int = 0, sleep_in_between=False) -> None:
        """
        Start the game. Play a certain amount of games each consisting of a certain amount of rounds.
        """
        progress = tqdm(total=games * rounds)

        for g in range(start_at_game, games):
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
                    await self._exchange_cards()
                self.agent_finish_order = []

                # Play the round
                for agent in self._get_play_order():
                    if sleep_in_between:
                        await asyncio.sleep(1)

                    await agent.make_move(self.table)

                    if sleep_in_between:
                        await asyncio.sleep(1)
                    # If the player finished this round award it by giving it its position.
                    if len(agent.player.hand) == 0:
                        self.agent_finish_order.append(agent)

                for agent in self.agents:
                    agent.round_end_callback(self.agent_finish_order, self.table)

                if self.verbose:
                    print(f'End order: {list(map(lambda x: x.player.player_id, self.agent_finish_order))}')
                    print('-' * 40)

                self.reset_temp_memory()

                if sleep_in_between:
                    await asyncio.sleep(1)

                triggered_early_stopping = False
                for agent in self.agents:
                    triggered_early_stopping = triggered_early_stopping or await agent.game_end_callback(g)
                if triggered_early_stopping:
                    break

                self.scum = self.agent_finish_order[-1]

        progress.close()

    # flake8: noqa: C901
    def on_move(self, agent: Agent, cards: List[Card]) -> None:
        """
        Handle move from Agent, We can be sure the agent can actually play the card.
        """
        # Save the move to memory to add to our network at the end of the game.
        cards_in_hand_vector: List[int] = map_cards_to_vector(agent.player.hand)
        cards_previous_move_vector: List[int] = map_cards_to_vector(
            self.table.last_move()[0] if self.table.last_move() else [])
        all_played_cards_vector: List[int] = map_cards_to_vector(
            list(chain.from_iterable([*map(lambda x: x[0], self.table.played_cards), *self.table.discard_pile])))

        input_vector = \
            np.array(cards_in_hand_vector + cards_previous_move_vector + all_played_cards_vector)[np.newaxis, :]

        if self.temp_memory[agent]:  # Set next state of previous move
            self.temp_memory[agent][-1][3] = input_vector

        calculated_move: int = map_cards_to_action(cards)

        if self.verbose:
            print('-' * 40)

        if not cards:
            # A Pass, disable the player for this round
            self.passed_agents[agent] = True
            #  print('Player passed')
            self.temp_memory[agent].append([input_vector, calculated_move, 0, None])

            for cb_agent in self.agents:
                cb_agent.move_played_callback([], agent.player)

            if self.verbose:
                print(f'Player {agent.player.player_id} has passed.')
            return None

        # A pass is a valid move.
        if len(cards) != 0:
            # WARNING: when playing with 2 decks of cards this is not sufficient.
            if not all(card in agent.player.hand for card in cards):
                self.passed_agents[agent] = True
                self.temp_memory[agent].append([input_vector, calculated_move, -10, None])

                for cb_agent in self.agents:
                    cb_agent.move_played_callback([], agent.player)

                if self.verbose:
                    print(f'Player {agent.player.player_id} can\'t make move and is forced to pass.')
                return None

        # Previous value should be lower
        if self.valid_move(cards, agent, debug=False):
            self.table.do_move(agent, cards)

            self.temp_memory[agent].append([input_vector, calculated_move, 0, None])

            for cb_agent in self.agents:
                cb_agent.move_played_callback(cards, agent.player)

            if self.verbose:
                print(f'Player {agent.player.player_id} makes move and has {len(agent.player.hand)} cards left:')
                print_cards(cards)
            return None
        else:
            self.passed_agents[agent] = True

            self.temp_memory[agent].append([input_vector, calculated_move, -10, None])

            for cb_agent in self.agents:
                cb_agent.move_played_callback([], agent.player)

            if self.verbose:
                print(f'Player {agent.player.player_id} plays invalid move and is forced to pass.')

            # punish at the end? => -0.01 from final reward per illegal move
            # Save move to memory when illegal-> with negative reward in already existing self.temp_memory[-1]?
            return None

    def valid_move(self, cards: List[Card], agent: Agent, debug=False) -> bool:

        last_move: Tuple[List[Card], Agent] = self.table.last_move()

        # If multiple cards are played length should be at least the same.
        if cards and last_move and len(cards) < len(last_move[0]):
            if debug:
                print('Not enough cards')
            return False

        # Check that the agent does not remain with only twos in his hand.
        remaining_cards = agent.player.hand[:]
        for card in cards:
            remaining_cards.remove(card)
        only_twos_remain: bool = True
        for card in remaining_cards:
            if card.get_value() != 15:
                only_twos_remain = False
        if only_twos_remain and len(remaining_cards) != 0:
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
            self.agents[i].cards_divided_callback()
        self.table.reset()

    async def _exchange_cards(self) -> None:
        # For now only the first and last player trade cards as this should not directly affect the learning.
        first: Agent = self.agent_finish_order[0]
        last: Agent = self.agent_finish_order[-1]
        preferred_cards: List[Card] = await first.get_preferred_card_order(self.table)

        # Hand best card from loser to winner
        card_index = 0
        while preferred_cards[card_index] not in last.player.hand:
            card_index += 1

        exchange_card: Card = preferred_cards[card_index]
        first.player.hand.append(exchange_card)
        last.player.hand.remove(exchange_card)

        # Hand lowest card from winner to loser
        exchange_card = await first.get_card_for_scum()
        first.player.hand.remove(exchange_card)
        last.player.hand.append(exchange_card)
        first.cards_exchanged_callback()
        last.cards_exchanged_callback()

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

            last_move_final_move: bool = (self.table.last_move() and len(self.table.last_move()[1].player.hand) == 0)

            if nr_skips >= len(self.agents) or \
                    (not last_move_final_move and
                     [len(agent.player.hand) == 0 or self.passed_agents[agent] for agent in self.agents].count(True) >=
                     len(self.agents) - 1):  # everyone except one has finished or passed, end trick.
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

            # If a new round is started, the scum of the previous round should start.
            if self.scum:
                while self.agent_iterator.get() != self.scum:
                    self.agent_iterator.next()
                self.scum = None

            yield self.agent_iterator.get()
        # The unfinished player comes last, add it to the last_played lis
        self.agent_finish_order.append(list(filter(lambda x: len(x.player.hand) > 0, self.agents))[0])

    def reset_temp_memory(self):
        for agent in self.agents:
            self.temp_memory[agent] = []
