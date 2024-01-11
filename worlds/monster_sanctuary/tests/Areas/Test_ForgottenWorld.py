from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class ForgottenWorldTests(TestArea):
    def test_jungle_shortcut(self):
        self.assertNotAccessible("ForgottenWorld_Jungle4", "forgotten_world_jungle_shortcut", [])
        self.assertNotAccessible("ForgottenWorld_Jungle4", "forgotten_world_jungle_shortcut",
                                 ["Forgotten World Jungle Shortcut"])
        self.assertAccessible("ForgottenWorld_Jungle4", "forgotten_world_jungle_shortcut",
                              ["Forgotten World Jungle Shortcut", "Goblin Miner"])

        self.assertNotAccessible("ForgottenWorld_JungleShortcut", "forgotten_world_jungle_shortcut", [])
        self.assertAccessible("ForgottenWorld_JungleShortcut", "forgotten_world_jungle_shortcut",
                              ["Goblin Miner"])

    def test_dracomer_lair_shortcut(self):
        # Test we can open up the shortcut
        self.assertNotAccessible("ForgottenWorld_DracomerLair", "forgotten_world_waters_shortcut", [])
        self.assertAccessible("ForgottenWorld_DracomerLair", "forgotten_world_waters_shortcut",
                              ["Yowie", "Koi"])

        # Test that once the shortcut is open we can get back through
        self.assertNotAccessible("ForgottenWorld_Waters1_Middle", "forgotten_world_waters_shortcut", [])
        self.assertAccessible("ForgottenWorld_Waters1_Middle", "ForgottenWorld_DracomerLair_2",
                              ["Koi", "Forgotten World Waters Shortcut"])

    def test_caves_shortcut(self):
        self.assertNotAccessible("ForgottenWorld_Caves11_Upper", "forgotten_world_caves_shortcut", [])
        self.assertAccessible("ForgottenWorld_Caves11_Upper", "forgotten_world_caves_shortcut",
                              ["Forgotten World Caves Shortcut"])

    def test_world_tree_progression(self):
        self.assertNotAccessible("ForgottenWorld_WorldTree", "ForgottenWorld_WorldTree_46100009", [])
        self.assertAccessible("ForgottenWorld_WorldTree", "ForgottenWorld_WorldTree_46100009",
                              ["Forgotten World Dracomer Defeated"])

    def test_wanderer_progression(self):
        self.assertNotAccessible("ForgottenWorld_WandererRoom", "ForgottenWorld_WandererRoom_45100110", [])
        self.assertNotAccessible("ForgottenWorld_WandererRoom", "ForgottenWorld_WandererRoom_45100110",
                                 ["Celestial Feather"])
        self.assertNotAccessible("ForgottenWorld_WandererRoom", "ForgottenWorld_WandererRoom_45100110",
                                 ["Celestial Feather", "Celestial Feather"])
        self.assertAccessible("ForgottenWorld_WandererRoom", "ForgottenWorld_WandererRoom_45100110",
                              ["Celestial Feather", "Celestial Feather", "Celestial Feather"])
