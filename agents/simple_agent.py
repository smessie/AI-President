from game.agent import Agent
from game.table import Table
from game.player import Player


class SimpleAgent(Agent):
    def __init__(self):
        super().__init__(Player())

    def make_move(self, table: Table) -> None:
        table.try_move(self, [sorted(self.player.hand)[0]])
