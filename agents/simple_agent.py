from game.agent import Agent
from game.table import Table


class SimpleAgent(Agent):
    def make_move(self, table: Table) -> None:
        table.make_move(self, [self.player.hand[0]])