from typing import Dict

from worlds.monster_sanctuary import items, locations, MonsterSanctuaryLocationCategory, MonsterSanctuaryItemCategory
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestPlotless(MonsterSanctuaryTestBase):
    options = {
        "skip_plot": 1
    }

    def test_mountain_path(self):
        self.assertTrue(self.multiworld.state.can_reach(
            "KeeperStronghold_WestStairwell",
            None,
            self.player))

    def test_stronghold(self):
        region = self.multiworld.get_region("StrongholdDungeon_Entrance", self.player)
        self.collect_all_but(["Blue Caves Story Complete", "Champion Defeated"], self.multiworld.state)
        self.assertTrue(self.multiworld.state.can_reach(
            region,
            None,
            self.player
        ))

    def test_blue_caves(self):
        location = self.multiworld.get_location("BlueCave_South5_29300061", self.player)
        self.collect_all_but(["Ostanes"], self.multiworld.state)
        self.assertTrue(self.multiworld.state.can_reach(
            location,
            None,
            self.player
        ))

    def test_horizon_beach(self):
        region = self.multiworld.get_region("HorizonBeach_TreasureCave1", self.player)
        self.collect_all_but(["Rescued Leonard"], self.multiworld.state)
        self.assertTrue(self.multiworld.state.can_reach(
            region,
            None,
            self.player
        ))

    def test_magma_chamber(self):
        location = self.multiworld.get_location("magma_chamber_lower_lava", self.player)
        self.collect_all_but(["Stronghold Dungeon Library Access"], self.multiworld.state)
        self.assertTrue(self.multiworld.state.can_reach(
            location,
            None,
            self.player
        ))