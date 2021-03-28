from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List

from game.agent import Agent
from game.player import Player
from game.table import Table
from util.cards import match_move, print_cards_string

if TYPE_CHECKING:
    from game.card import Card


class DiscordAgent(Agent):
    def __init__(self, discord_bot, channel, player_name: str = None):
        super().__init__(Player(player_name if player_name is not None and player_name != '' else 'DiscordAgent'))
        self.discord_bot = discord_bot
        self.channel = channel

    async def make_move(self, table: Table) -> None:
        self.print_whitespace()

        possible_moves: List[List[Card]] = self.player.get_all_possible_moves(table, self)

        self.print_cards('Your cards:\n')
        await asyncio.sleep(1)

        move = match_move(await self.discord_bot.read_string_input('Enter move to take: ', self.channel),
                          possible_moves)
        while move is None:
            self.discord_bot.print('Move is invalid! Try again. (Enter 0 to pass)', self.channel)
            move = match_move(await self.discord_bot.read_string_input('Enter move to take: ', self.channel),
                              possible_moves)
        table.try_move(self, move)

    def move_played_callback(self, move: List[Card], player: Player):
        if move:
            to_print = ''
            to_print += f'{player.get_player_name()} made following move and has {len(player.hand)} cards left:\n'
            to_print += print_cards_string(move)
            self.discord_bot.print(to_print, self.channel)
        else:
            self.discord_bot.print(f'{player.get_player_name()} passed.', self.channel)

    def round_end_callback(self, agent_finish_order: List[Agent], table: Table):
        self.print_whitespace()
        to_print = '**Round has ended! Here is the ranking:**\n'
        for i, agent in enumerate(agent_finish_order):
            to_print += f'**#{i + 1}. {agent.player.get_player_name()}**\n'
        self.discord_bot.print(to_print, self.channel)
        self.print_whitespace()

    async def game_end_callback(self, game_nr: int) -> bool:
        self.print_whitespace()
        self.discord_bot.print('Aww, the game is already over :(', self.channel)
        keep_playing = await self.discord_bot.read_bool_input('Lets play another game? (y/n)', self.channel)
        return not keep_playing

    def trick_end_callback(self, table: Table, playing_agents: List[Agent]):
        self.discord_bot.print(f'Let\'s clear the deck. On to the next trick! '
                               f'{", ".join(map(lambda agent: agent.player.get_player_name(), playing_agents))}'
                               f' are still playing.', self.channel)

    def print_whitespace(self):
        self.discord_bot.print('- \n' + ('-' * 40) + '\n- \n', self.channel)

    def cards_divided_callback(self):
        self.print_cards('New game started! Your cards:\n')

    def print_cards(self, message):
        to_print = message
        move_string = print_cards_string(sorted(self.player.hand, key=lambda x: x.value))
        if len(to_print) + len(move_string) > 1950:
            self.discord_bot.print(to_print, self.channel)
            to_print = ''
        to_print += move_string
        self.discord_bot.print(to_print, self.channel)

    async def get_preferred_card_order(self, table: Table) -> List[Card]:
        self.print_whitespace()
        self.discord_bot.print('You are President! Give the cards in the order in which you would prefer to get them '
                               'from the scum. If you would prefer to get a 2 and alternatively an ace, fill in 2A and '
                               'so on, finishing with the card you would least like to have. Cards you do not mention '
                               'are added to the back of the row.', self.channel)
        card_order: str = await self.discord_bot.read_string_input('Enter cards: ', self.channel)
        possible_cards: List[Card] = sorted(table.deck.card_stack, reverse=True)
        preferred_cards = []
        for card in list(card_order.upper()):
            i = 0
            while i < len(possible_cards):
                if possible_cards[i].get_char_value() == card:
                    matching_card = possible_cards[i]
                    preferred_cards.append(matching_card)
                    possible_cards.remove(matching_card)
                else:
                    i += 1
        preferred_cards.extend(possible_cards)
        return preferred_cards

    async def get_card_for_scum(self) -> Card:
        card = None
        while card is None:
            input_card: str = await self.discord_bot.read_string_input('Enter card to give to the scum: ', self.channel)
            cards = match_move(input_card, [[card] for card in self.player.hand])
            if cards and len(cards) == 1:
                card = cards[0]
            else:
                self.discord_bot.print('Card is invalid! Try again.', self.channel)
        return card

    def cards_exchanged_callback(self):
        self.print_whitespace()
        self.print_cards('The cards between the President and scum have been exchanged. These are your new cards:')
