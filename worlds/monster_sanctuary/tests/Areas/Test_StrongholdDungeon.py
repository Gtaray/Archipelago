from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class StrongholdDungeonTests(TestArea):
    def test_traversal(self):
        # Make sure that if the player falls into the bottom half of this room, that they can get back out
        self.starting_regions = ["StrongholdDungeon_East1_SW"]
        self.run_tests([
            ["stronghold_dungeon_east_unlocked", False, []],
            ["stronghold_dungeon_east_unlocked", False, ["Stronghold Dungeon key"]],
            ["stronghold_dungeon_east_unlocked", True, ["Double Jump Boots", "Stronghold Dungeon key"]],
            ["stronghold_dungeon_east_unlocked", True, ["Kongamato", "Stronghold Dungeon key"]],
        ])

    def test_keys(self):
        self.starting_regions = ["StrongholdDungeon_South3"]
        self.run_tests([
            ["stronghold_dungeon_south_unlocked", False, []],
            ["stronghold_dungeon_south_unlocked", True, ["Stronghold Dungeon key"]],
            ["stronghold_dungeon_south_unlocked", True, ["Stronghold Dungeon South Unlocked"]],
            ["stronghold_dungeon_south_unlocked", False, ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key"]],
            ["stronghold_dungeon_south_unlocked", True, ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key",
                                                         "Stronghold Dungeon key"]],
        ])

        self.starting_regions = ["StrongholdDungeon_East1_NE", "StrongholdDungeon_East1_NW"]
        self.run_tests([
            ["stronghold_dungeon_east_unlocked", False, []],
            ["stronghold_dungeon_east_unlocked", True, ["Stronghold Dungeon key"]],
            ["stronghold_dungeon_east_unlocked", True, ["Stronghold Dungeon East Unlocked"]],
            ["stronghold_dungeon_east_unlocked", False, ["Stronghold Dungeon South Unlocked",
                                                         "Stronghold Dungeon key"]],
            ["stronghold_dungeon_east_unlocked", True, ["Stronghold Dungeon South Unlocked", "Stronghold Dungeon key",
                                                        "Stronghold Dungeon key"]],
        ])
