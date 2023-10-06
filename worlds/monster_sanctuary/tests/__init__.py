from test.TestBase import WorldTestBase
from test.general.TestImplemented import TestImplemented
from worlds.monster_sanctuary import data_importer


class MonsterSanctuaryTestBase(WorldTestBase):
    game = "Monster Sanctuary"
    player: int = 1

