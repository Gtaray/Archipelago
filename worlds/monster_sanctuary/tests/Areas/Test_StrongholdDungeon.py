from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class StrongholdDungeonTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_east1_traversal(self):
        # Make sure that if the player falls into the bottom half of this room, that they can get back out
        self.assertNotAccessible("StrongholdDungeon_East1_SW", "stronghold_dungeon_east_unlocked", [])
        self.assertNotAccessible("StrongholdDungeon_East1_SW", "stronghold_dungeon_east_unlocked",
                                 ["Stronghold Dungeon key"])

        self.assertAccessible("StrongholdDungeon_East1_SW", "stronghold_dungeon_east_unlocked",
                              ["Double Jump Boots", "Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_East1_SW", "stronghold_dungeon_east_unlocked",
                              ["Kongamato", "Stronghold Dungeon key"])

    def test_south_locked_door(self):
        self.assertNotAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked", [])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon South Unlocked"])

        self.assertNotAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                                 ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key", "Stronghold Dungeon key"])

    def test_east_locked_door(self):
        # Test from northeast
        self.assertNotAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked", [])
        self.assertAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon East Unlocked"])

        self.assertNotAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked",
                                 ["Stronghold Dungeon South Unlocked", "Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon South Unlocked", "Stronghold Dungeon key", "Stronghold Dungeon key"])

        # Test from northwest
        self.assertNotAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked", [])
        self.assertAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon East Unlocked"])

        self.assertNotAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked",
                                 ["Stronghold Dungeon South Unlocked", "Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked",
                              ["Stronghold Dungeon South Unlocked", "Stronghold Dungeon key", "Stronghold Dungeon key"])


class StrongholdDungeonMinimumLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_east_accessible_with_no_keys(self):
        self.assertAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked", [])
        self.assertAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked", [])

    def test_south_locked_door(self):
        self.assertNotAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked", [])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon South Unlocked"])

        self.assertNotAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                                 ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key"])
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked",
                              ["Stronghold Dungeon East Unlocked", "Stronghold Dungeon key", "Stronghold Dungeon key"])


class StrongholdDungeonNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_east_accessible_with_no_keys(self):
        self.assertAccessible("StrongholdDungeon_East1_NE", "stronghold_dungeon_east_unlocked", [])
        self.assertAccessible("StrongholdDungeon_East1_NW", "stronghold_dungeon_east_unlocked", [])

    def test_south_accessible_with_no_keys(self):
        self.assertAccessible("StrongholdDungeon_South3", "stronghold_dungeon_south_unlocked", [])