from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class BlueCavesTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_switches_locked_door(self):
        self.assertNotAccessible("BlueCave_North1", "blue_cave_switches_unlocked", [])
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked",
                              ["Blue Cave key"])
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked",
                              ["Blue Caves Switches Unlocked"])

        # Check that used keys allow or disallow access
        # In this scenario, we have 1 key, and it was used to open the champion door.
        self.assertNotAccessible("BlueCave_North1", "blue_cave_switches_unlocked",
                                 ["Blue Caves Champion Unlocked", "Blue Cave key"])
        # In this scenario, we have 2 keys, and one was used to open the champion door
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked",
                              ["Blue Caves Champion Unlocked", "Blue Cave key", "Blue Cave key"])
        # In this scenario, we have 3 keys, and two were used to open other doors
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked",
                              ["Blue Caves Champion Unlocked", "Blue Caves South Unlocked",
                               "Blue Cave key", "Blue Cave key", "Blue Cave key"])

    def test_south_locked_door(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked", [])
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                                 ["Blue Caves Champion Unlocked"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Caves South Unlocked"])

        # Check that used keys allow or disallow access
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                                 ["Blue Caves Switches Unlocked", "Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Caves Switches Unlocked", "Blue Cave key", "Blue Cave key"])

        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                                 ["Blue Caves Champion Unlocked", "Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Caves Champion Unlocked", "Blue Cave key", "Blue Cave key"])

        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                                 ["Blue Caves Switches Unlocked", "Blue Caves Champion Unlocked",
                                  "Blue Cave key", "Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Caves Switches Unlocked", "Blue Caves Champion Unlocked",
                               "Blue Cave key", "Blue Cave key", "Blue Cave key"])

    def test_champion_door_requires_double_jump(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                                 ["Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Cave key", "Double Jump Boots"])

    def test_champion_locked_door(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                                 ["Double Jump Boots"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Cave key", "Double Jump Boots"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Caves Champion Unlocked", "Double Jump Boots"])

        # Check that used keys allow or disallow access
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                                 ["Blue Caves Switches Unlocked", "Blue Cave key", "Double Jump Boots"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Caves Switches Unlocked", "Blue Cave key", "Blue Cave key", "Double Jump Boots"])

        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                                 ["Blue Caves South Unlocked", "Blue Cave key", "Double Jump Boots"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Caves South Unlocked", "Blue Cave key", "Blue Cave key", "Double Jump Boots"])

        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                                 ["Blue Caves Switches Unlocked", "Blue Caves South Unlocked",
                                  "Blue Cave key", "Blue Cave key", "Double Jump Boots"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked",
                              ["Blue Caves Switches Unlocked", "Blue Caves South Unlocked",
                               "Blue Cave key", "Blue Cave key", "Blue Cave key", "Double Jump Boots"])

    def test_mountain_path_shortcut(self):
        # Test that the shortcut can be accessed from the blue caves side
        self.assertAccessible("BlueCave_ChampionRoom2", "blue_cave_champion_room_2_west_shortcut", [])

        # Test tha the shortcut can only be used if the blue cave side has been unlocked
        self.assertNotAccessible("MountainPath_Center6_Lower", "blue_cave_champion_room_2_west_shortcut", [])
        self.assertAccessible("MountainPath_Center6_Lower", "blue_cave_champion_room_2_west_shortcut",
                              ["Blue Caves to Mountain Path Shortcut"])

    def test_sanctuary_token_check(self):
        self.assertNotAccessible("BlueCave_South5", "BlueCave_South5_29300061", [])
        self.assertAccessible("BlueCave_South5", "BlueCave_South5_29300061", ["Ostanes"])


class BlueCavesMinimalLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_champion_accessible_with_no_keys(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked", [])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked", ["Double Jump Boots"])

    def test_south_locked_door(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked", [])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Cave key"])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked",
                              ["Blue Caves South Unlocked"])

    def test_switches_accessible_with_no_keys(self):
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked", [])


class BlueCavesNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_champion_accessible_with_no_keys(self):
        self.assertNotAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked", [])
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_champion_unlocked", ["Double Jump Boots"])

    def test_south_accessible_with_no_keys(self):
        self.assertAccessible("BlueCave_CentralPart", "blue_cave_south_unlocked", [])

    def test_switches_accessible_with_no_keys(self):
        self.assertAccessible("BlueCave_North1", "blue_cave_switches_unlocked", [])


class BlueCavesPlotlessTests(TestArea):
    options = {
        "skip_plot": 1
    }

    def test_sanctuary_token_check(self):
        self.assertAccessible("BlueCave_South5", "BlueCave_South5_29300061", [])
