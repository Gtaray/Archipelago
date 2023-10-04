from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MysticWorkshopTests(TestArea):
    def test_keys(self):
        self.starting_regions = ["MysticalWorkshop_North6"]
        self.run_tests([
            ["mystical_workshop_north_unlocked", False, []],
            ["mystical_workshop_north_unlocked", False, ["Double Jump Boots", "Mystical Workshop key"]],
            ["mystical_workshop_north_unlocked", False, ["Mystical Workshop key", "Mystical Workshop key",
                                                         "Double Jump Boots"]],
            ["mystical_workshop_north_unlocked", True, ["Double Jump Boots", "Mystical Workshop key",
                                                        "Mystical Workshop key", "Mystical Workshop key"]],
            ["mystical_workshop_north_unlocked", True, ["Double Jump Boots", "Mystical Workshop North Unlocked"]],
        ])

    def test_shortcuts(self):
        self.starting_regions = ["MysticalWorkshop_North4_Shortcut"]
        self.run_tests([
            ["mystical_workshop_north_shortcut", False, []],
            ["mystical_workshop_north_unlocked", True, ["Mystical Workshop North Shortcut"]]
        ])

    def test_progression(self):
        self.starting_regions = ["MysticalWorkshop_South1"]
        self.run_tests([
            ["abandoned_tower_access", False, []],
            ["abandoned_tower_access", False, ["Double Jump Boots", "Silvaero"]],
            ["abandoned_tower_access", False, ["Double Jump Boots", "Silvaero", "Mystical Workshop key"]],
            ["abandoned_tower_access", False, ["Double Jump Boots", "Silvaero", "Mystical Workshop key",
                                               "Mystical Workshop key"]],
            ["abandoned_tower_access", True, ["Double Jump Boots", "Silvaero", "Mystical Workshop key",
                                              "Mystical Workshop key", "Mystical Workshop key"]],
            ["abandoned_tower_access", True, ["Double Jump Boots", "Silvaero", "Mystical Workshop North Unlocked"]]
        ])
