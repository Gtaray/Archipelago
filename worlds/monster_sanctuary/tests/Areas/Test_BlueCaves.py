from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class BlueCavesTests(TestArea):
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


