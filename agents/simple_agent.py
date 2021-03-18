from game.agent import Agent
from game.player import Player
from game.table import Table


class SimpleAgent(Agent):
    def __init__(self):
        super().__init__(Player())

    async def make_move(self, table: Table) -> None:
        table.try_move(self, [sorted(self.player.hand)[0]])
