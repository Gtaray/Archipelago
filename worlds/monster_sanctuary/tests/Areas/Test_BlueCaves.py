from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class BlueCavesTests(TestArea):
    def test_keys(self):
        self.starting_regions = ["BlueCave_North1"]

        self.run_tests([
            ["blue_cave_switches_unlocked", False, []],
            ["blue_cave_switches_unlocked", True, ["Blue Cave key"]],
            ["blue_cave_switches_unlocked", True, ["Blue Caves Switches Unlocked"]],

            # Test whether used keys allow or disallow access
            ["blue_cave_switches_unlocked", False, ["Blue Caves Key Used", "Blue Cave key"]],
            ["blue_cave_switches_unlocked", True, ["Blue Caves Key Used", "Blue Cave key", "Blue Cave key"]]
        ])

        self.starting_regions = ["BlueCave_CentralPart"]
        self.run_tests([
            ["blue_cave_south_unlocked", False, []],
            ["blue_cave_south_unlocked", False, ["Blue Caves Champion Unlocked"]],
            ["blue_cave_south_unlocked", True, ["Blue Caves South Unlocked"]],
            ["blue_cave_south_unlocked", True, ["Blue Cave key"]],
            ["blue_cave_south_unlocked", False, ["Blue Caves Key Used", "Blue Cave key"]],
            ["blue_cave_south_unlocked", True, ["Blue Caves Key Used", "Blue Cave key", "Blue Cave key"]],

            ["blue_cave_champion_unlocked", False, []],
            ["blue_cave_champion_unlocked", False, ["Blue Caves South Unlocked"]],
            ["blue_cave_champion_unlocked", True, ["Blue Caves Champion Unlocked", "Double Jump Boots"]],
            ["blue_cave_champion_unlocked", True, ["Blue Cave key", "Double Jump Boots"]],
            ["blue_cave_champion_unlocked", False, ["Blue Caves Key Used", "Blue Cave key",
                                                    "Double Jump Boots"]],
            ["blue_cave_champion_unlocked", True, ["Blue Caves Key Used", "Blue Cave key", "Blue Cave key",
                                                   "Double Jump Boots"]]
        ])

    def test_shortcuts(self):
        self.starting_regions = ["MountainPath_Center6_Lower"]
        self.run_tests([
            ["blue_cave_champion_room_2_west_shortcut", False, []],
            ["blue_cave_champion_room_2_west_shortcut", True, ["Blue Caves to Mountain Path Shortcut"]]
        ])

        self.starting_regions = ["BlueCave_ChampionRoom2"]
        self.run_tests([
            ["blue_cave_champion_room_2_west_shortcut", True, []]
        ])
