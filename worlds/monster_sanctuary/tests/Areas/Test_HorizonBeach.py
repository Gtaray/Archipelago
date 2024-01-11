from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class HorizonBeachTests(TestArea):
    def test_center_shortcut(self):
        self.assertNotAccessible("HorizonBeach_Center1", "horizon_beach_center_shortcut", [])
        self.assertNotAccessible("HorizonBeach_Center1", "horizon_beach_center_shortcut",
                                 ["Horizon Beach Center Shortcut"])

        self.assertAccessible("HorizonBeach_Center1", "horizon_beach_center_shortcut",
                              ["Koi"])

    def test_forgotten_world_shortcut(self):
        self.assertNotAccessible("HorizonBeach_Center5", "forgotten_world_to_horizon_beach_shortcut", [])
        self.assertNotAccessible("HorizonBeach_Center5", "forgotten_world_to_horizon_beach_shortcut",
                                 ["Forgotten World to Horizon Beach Shortcut"])
        self.assertNotAccessible("HorizonBeach_Center5", "forgotten_world_to_horizon_beach_shortcut",
                                 ["Brutus"])

        self.assertAccessible("HorizonBeach_Center5", "forgotten_world_to_horizon_beach_shortcut",
                              ["Forgotten World to Horizon Beach Shortcut", "Brutus"])

    def test_rescue_leonard(self):
        self.assertNotAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard", [])
        self.assertNotAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard",
                                 ["Kongamato"])
        self.assertNotAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard",
                                 ["Koi"])
        self.assertNotAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard",
                                 ["Goblin King Defeated"])

        self.assertAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard",
                              ["Koi", "Kongamato", "Goblin King Defeated"])
        self.assertAccessible("HorizonBeach_West1", "horizon_beach_rescue_leonard",
                              ["Koi", "Vaero", "Tree of Evolution Access", "Silver Feather", "Goblin King Defeated"])

    def test_can_reach_champion(self):
        self.assertNotAccessible("HorizonBeach_West1", "HorizonBeach_Champion_Champion", [])
        self.assertNotAccessible("HorizonBeach_West1", "HorizonBeach_Champion_Champion",
                                 ["Koi"])
        self.assertNotAccessible("HorizonBeach_West1", "HorizonBeach_Champion_Champion",
                                 ["Rescued Leonard"])
        self.assertNotAccessible("HorizonBeach_West1", "HorizonBeach_Champion_Champion",
                                 ["Goblin King Defeated"])

        self.assertAccessible("HorizonBeach_West1", "HorizonBeach_Champion_Champion",
                              ["Koi", "Rescued Leonard", "Goblin King Defeated"])
