import unittest

from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class SunPalaceTests(TestArea):
    def test_raising_center(self):
        self.starting_regions = ["SunPalace_Center"]
        self.run_tests([
            ["sun_palace_raise_center_1", False, []],
            ["sun_palace_raise_center_1", True, ["Double Jump Boots"]],
            ["sun_palace_raise_center_1", True, ["Silvaero"]],

            ["sun_palace_raise_center_2", False, []],
            ["sun_palace_raise_center_2", True, ["Krakaturtle"]],
            ["sun_palace_raise_center_2", True, ["Sun Palace Lower Water", "Krakaturtle"]],
            ["sun_palace_raise_center_2", True, ["Sun Palace Lower Water", "Double Jump Boots"]],
            ["sun_palace_raise_center_2", True, ["Sun Palace Lower Water", "Sun Palace Lower Water", "Silvaero"]],

            ["sun_palace_raise_center_3", False, []],
            ["sun_palace_raise_center_3", True, ["Krakaturtle"]],
            ["sun_palace_raise_center_3", True, ["Koi", "Vaero"]],
            ["sun_palace_raise_center_3", True, ["Koi", "Double Jump Boots"]],
            ["sun_palace_raise_center_3", True, ["Sun Palace Lower Water", "Sun Palace Lower Water",
                                                 "Double Jump Boots"]],
            ["sun_palace_raise_center_3", True, ["Sun Palace Lower Water", "Sun Palace Lower Water",
                                                 "Silvaero"]]
        ])

    def test_lowering_water(self):
        self.starting_regions = ["SunPalace_Center"]
        self.run_tests([
            ["sun_palace_lower_water_1", False, []],
            ["sun_palace_lower_water_1", True, ["Sun Palace Raise Center"]],

            ["sun_palace_lower_water_2", False, []],
            ["sun_palace_lower_water_2", True, ["Sun Palace Raise Center", "Sun Palace Raise Center"]],
        ])

    # We don't need to test if we can get to the shortcut areas normally
    # because the above tests for the raise_center flags are in the same spots
    # as the shortcuts. So if we can get to one, we can get to the other
    def test_shortcuts(self):
        self.starting_regions = ["SunPalace_Center"]
        self.run_tests([
            ["sun_palace_east_shortcut", False, []],
            ["sun_palace_east_shortcut", True, ["Sun Palace East Shortcut"]],

            ["sun_palace_west_shortcut", False, []],
            ["sun_palace_west_shortcut", True, ["Sun Palace West Shortcut"]]
        ])
