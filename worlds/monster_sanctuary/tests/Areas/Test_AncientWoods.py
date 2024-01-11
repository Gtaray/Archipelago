from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class AncientWoodsTests(TestArea):
    def test_center_locked_door(self):
        # Test from Center2
        self.assertNotAccessible("AncientWoods_Center2", "ancient_woods_center_unlocked", [])
        self.assertNotAccessible("AncientWoods_Center2", "ancient_woods_center_unlocked",
                                 ["Ancient Woods key"])
        self.assertNotAccessible("AncientWoods_Center2", "ancient_woods_center_unlocked",
                                 ["Ancient Woods key", "Ancient Woods key", "Ancient Woods North Unlocked"])

        self.assertAccessible("AncientWoods_Center2", "ancient_woods_center_unlocked",
                              ["Ancient Woods key", "Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center2", "ancient_woods_center_unlocked",
                              ["Ancient Woods Center Unlocked"])

        # Test from Center5
        self.assertNotAccessible("AncientWoods_Center5", "ancient_woods_center_unlocked", [])
        self.assertNotAccessible("AncientWoods_Center5", "ancient_woods_center_unlocked",
                                 ["Ancient Woods key"])
        self.assertNotAccessible("AncientWoods_Center5", "ancient_woods_center_unlocked",
                                 ["Ancient Woods key", "Ancient Woods key", "Ancient Woods North Unlocked"])

        self.assertAccessible("AncientWoods_Center5", "ancient_woods_center_unlocked",
                              ["Ancient Woods key", "Ancient Woods key"])
        self.assertAccessible("AncientWoods_Center5", "ancient_woods_center_unlocked",
                              ["Ancient Woods Center Unlocked"])

    def test_north_locked_door(self):
        self.assertNotAccessible("AncientWoods_North2", "ancient_woods_north_unlocked", [])
        self.assertNotAccessible("AncientWoods_North2", "ancient_woods_north_unlocked",
                                 ["Ancient Woods key", "Ancient Woods Center Unlocked"])
        self.assertNotAccessible("AncientWoods_North2", "ancient_woods_north_unlocked",
                                 ["Ancient Woods key", "Ancient Woods key", "Ancient Woods Center Unlocked"])

        self.assertAccessible("AncientWoods_North2", "ancient_woods_north_unlocked",
                              ["Ancient Woods key"])
        self.assertAccessible("AncientWoods_North2", "ancient_woods_north_unlocked",
                              ["Ancient Woods North Unlocked"])
        self.assertAccessible("AncientWoods_North2", "ancient_woods_north_unlocked",
                              ["Ancient Woods key", "Ancient Woods key", "Ancient Woods key", "Ancient Woods Center Unlocked"])

    def test_east_shortcut(self):
        self.assertNotAccessible("AncientWoods_East1", "ancient_woods_east_shortcut", [])
        self.assertAccessible("AncientWoods_East1", "ancient_woods_east_shortcut", ["Ancient Woods East Shortcut"])

    def test_magma_chamber_shortcut(self):
        self.assertNotAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2", [])
        self.assertNotAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2", ["Ancient Woods to Magma Chamber Shortcut"])
        self.assertAccessible("AncientWoods_South1_Lower", "ancient_woods_magma_chamber_2",
                              ["Ancient Woods to Magma Chamber Shortcut", "Ancient Woods to Magma Chamber Shortcut"])
