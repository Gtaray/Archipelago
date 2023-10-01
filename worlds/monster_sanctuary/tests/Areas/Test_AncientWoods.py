from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class AncientWoodsTests(TestArea):
    def test_keys(self):
        self.starting_regions = ["AncientWoods_Center2"]
        self.run_tests([
            ["ancient_woods_center_unlocked", False, []],
            ["ancient_woods_center_unlocked", False, ["Ancient Woods key"]],
            ["ancient_woods_center_unlocked", True, ["Ancient Woods key", "Ancient Woods key"]],
            ["ancient_woods_center_unlocked", True, ["Ancient Woods Center Unlocked"]],
        ])

        self.starting_regions = ["AncientWoods_Center5"]
        self.run_tests([
            ["ancient_woods_center_unlocked", False, []],
            ["ancient_woods_center_unlocked", False, ["Ancient Woods key"]],
            ["ancient_woods_center_unlocked", True, ["Ancient Woods key", "Ancient Woods key"]],
            ["ancient_woods_center_unlocked", True, ["Ancient Woods Center Unlocked"]],
        ])

        self.starting_regions = ["AncientWoods_North2"]
        self.run_tests([
            ["ancient_woods_north_unlocked", False, []],
            ["ancient_woods_north_unlocked", True, ["Ancient Woods key"]],
            ["ancient_woods_north_unlocked", True, ["Ancient Woods North Unlocked"]],
        ])

    # This will fail until magma caverns is done
    def test_shortcuts(self):
        self.starting_regions = ["AncientWoods_East1"]
        self.run_tests([
            ["ancient_woods_east_shortcut", False, []],
            ["ancient_woods_east_shortcut", True, ["Ancient Woods East Shortcut"]]
        ])

        self.starting_regions = ["AncientWoods_South1_Lower"]
        self.run_tests([
            ["ancient_woods_magma_chamber_2", False, []],
            ["ancient_woods_magma_chamber_2", False, ["Ancient Woods to Magma Chamber Shortcut"]],
            ["ancient_woods_magma_chamber_2", True, ["Ancient Woods to Magma Chamber Shortcut",
                                                      "Ancient Woods to Magma Chamber Shortcut"]]
        ])
