from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class HorizonBeachTests(TestArea):
    def test_shortcuts(self):
        self.starting_regions = ["HorizonBeach_Center1"]
        self.run_tests([
            ["horizon_beach_center_shortcut", False, []],
            ["horizon_beach_center_shortcut", False, ["Horizon Beach Center Shortcut"]],
            ["horizon_beach_center_shortcut", True, ["Koi"]],
            ["horizon_beach_center_shortcut", True, ["Horizon Beach Center Shortcut", "Koi"]]
        ])

        self.starting_regions = ["HorizonBeach_Center5"]
        self.run_tests([
            ["forgotten_world_to_horizon_beach_shortcut", False, []],
            ["forgotten_world_to_horizon_beach_shortcut", True, ["Forgotten World to Horizon Beach Shortcut", "Brutus"]]
        ])

    def test_progression(self):
        self.starting_regions = ["HorizonBeach_West1"]
        self.run_tests([
            ["horizon_beach_rescue_leonard", False, []],
            ["horizon_beach_rescue_leonard", False, ["Silvaero"]],
            ["horizon_beach_rescue_leonard", False, ["Koi"]],
            ["horizon_beach_rescue_leonard", True, ["Koi", "Silvaero"]],

            ["HorizonBeach_Champion_Champion", False, []],
            ["HorizonBeach_Champion_Champion", False, ["Koi"]],
            ["HorizonBeach_Champion_Champion", False, ["Rescued Leonard"]],
            ["HorizonBeach_Champion_Champion", True, ["Koi", "Rescued Leonard"]],
        ])
