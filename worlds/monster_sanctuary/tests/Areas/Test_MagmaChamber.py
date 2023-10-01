from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MagmaChamberTests(TestArea):
    def test_shortcuts(self):
        self.starting_regions = ["MagmaChamber_North8_East"]
        self.run_tests([
            ["magma_chamber_north_shortcut", False, []],
            ["magma_chamber_north_shortcut", True, ["Magma Chamber North Shortcut"]]
        ])

        self.starting_regions = ["MagmaChamber_South3_West"]
        self.run_tests([
            ["magma_chamber_south_shortcut", False, []],
            ["magma_chamber_south_shortcut", True, ["Magma Chamber South Shortcut"]]
        ])

        self.starting_regions = ["MagmaChamber_Center4_West"]
        self.run_tests([
            ["magma_chamber_center_shortcut", False, []],
            ["magma_chamber_center_shortcut", True, ["Magma Chamber Center Shortcut"]]
        ])

        self.starting_regions = ["MagmaChamber_East1"]
        self.run_tests([
            ["magma_chamber_east_shortcut", False, []],
            ["magma_chamber_east_shortcut", True, ["Magma Chamber East Shortcut"]]
        ])

        self.starting_regions = ["MagmaChamber_South9_East"]
        self.run_tests([
            ["forgotten_world_to_magma_chamber_shortcut", False, []],
            ["forgotten_world_to_magma_chamber_shortcut", True, ["Forgotten World to Magma Chamber Shortcut"]]
        ])

    def test_keys(self):
        self.starting_regions = ["MagmaChamber_AlchemistLab_West"]
        self.run_tests([
            ["magma_chamber_alchemist_lab_unlocked", False, []],
            ["magma_chamber_alchemist_lab_unlocked", True, ["Magma Chamber key"]],
            ["magma_chamber_alchemist_lab_unlocked", False, ["Magma Chamber Key Used", "Magma Chamber key"]],
            ["magma_chamber_alchemist_lab_unlocked", True, ["Magma Chamber Alchemist Lab Unlocked"]]
        ])

        self.starting_regions = ["MagmaChamber_Center9_Middle"]
        self.run_tests([
            ["magma_chamber_mozzie_room_unlocked", False, []],
            ["magma_chamber_mozzie_room_unlocked", True, ["Magma Chamber key"]],
            ["magma_chamber_mozzie_room_unlocked", False, ["Magma Chamber Key Used", "Magma Chamber key"]],
            ["magma_chamber_mozzie_room_unlocked", True, ["Magma Chamber Mozzie Room Unlocked"]]
        ])

    def test_progression(self):
        self.starting_regions = ["MagmaChamber_Runestone"]
        self.run_tests([
            ["magma_chamber_lower_lava", False, []],
            ["magma_chamber_lower_lava", False, ["Stronghold Dungeon Library Access"]],
            ["magma_chamber_lower_lava", False, ["Runestone Shard"]],
            ["magma_chamber_lower_lava", True, ["Stronghold Dungeon Library Access", "Runestone Shard"]]
        ])

        self.starting_regions = ["MagmaChamber_Center2_Middle"]
        self.run_tests([
            ["MagmaChamber_Center2_Lower_16", False, []],
            ["MagmaChamber_Center2_Lower_16", True, ["Magma Chamber Lowered Lava"]]
        ])
