from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class AbandonedTowerTests(TestArea):
    def test_shortcuts(self):
        self.starting_regions = ["AbandonedTower_South8"]
        self.run_tests([
            ["abandoned_tower_south_shortcut", False, []],
            ["abandoned_tower_south_shortcut", True, ["Abandoned Tower South Shortcut"]]
        ])

        self.starting_regions = ["AbandonedTower_Center10"]
        self.run_tests([
            ["abandoned_tower_center_shortcut", False, []],
            ["abandoned_tower_center_shortcut", True, ["Abandoned Tower Center Shortcut"]]
        ])

    def test_progression(self):
        self.starting_regions = ["AbandonedTower_Entrance"]
        self.run_tests([
            ["mad_lord_defeated", False, []],
            ["mad_lord_defeated", False, ["Key of Power"]],
            ["mad_lord_defeated", False, ["Double Jump Boots"]],
            ["mad_lord_defeated", True, ["Key of Power", "Double Jump Boots"]]
        ])
