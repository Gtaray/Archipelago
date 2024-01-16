from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MagmaChamberTests(TestArea):
    options = {
        "remove_locked_doors": 0
    }

    def test_north_shortcut(self):
        self.assertNotAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut", [])
        self.assertAccessible("MagmaChamber_North8_East", "magma_chamber_north_shortcut",
                              ["Magma Chamber North Shortcut"])

    def test_south_shortcut(self):
        self.assertNotAccessible("MagmaChamber_South3_West", "magma_chamber_south_shortcut", [])
        self.assertAccessible("MagmaChamber_South3_West", "magma_chamber_south_shortcut",
                              ["Magma Chamber South Shortcut"])

    def test_center_shortcut(self):
        self.assertNotAccessible("MagmaChamber_Center4_West", "magma_chamber_center_shortcut", [])
        self.assertAccessible("MagmaChamber_Center4_West", "magma_chamber_center_shortcut",
                              ["Magma Chamber Center Shortcut"])

    def test_east_shortcut(self):
        self.assertNotAccessible("MagmaChamber_East1", "magma_chamber_east_shortcut", [])
        self.assertAccessible("MagmaChamber_East1", "magma_chamber_east_shortcut",
                              ["Magma Chamber East Shortcut"])

    def test_forgotten_world_shortcut(self):
        self.assertNotAccessible("MagmaChamber_South9_East", "forgotten_world_to_magma_chamber_shortcut", [])
        self.assertAccessible("MagmaChamber_South9_East", "forgotten_world_to_magma_chamber_shortcut",
                              ["Forgotten World to Magma Chamber Shortcut"])

    def test_alchemist_lab_locked_door(self):
        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked", [])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber key"])

        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                                 ["Magma Chamber Mozzie Room Unlocked", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber Mozzie Room Unlocked", "Magma Chamber key", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber Alchemist Lab Unlocked"])

    def test_mozzie_room_locked_door(self):
        self.assertNotAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked", [])
        self.assertAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked",
                              ["Magma Chamber key"])

        self.assertNotAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked",
                                 ["Magma Chamber Alchemist Lab Unlocked", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked",
                              ["Magma Chamber Alchemist Lab Unlocked", "Magma Chamber key", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked",
                              ["Magma Chamber Mozzie Room Unlocked"])

    def test_runestone(self):
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava", [])
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                                 ["Stronghold Dungeon Library Access"])
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                                 ["Runestone Shard"])
        self.assertAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",
                              ["Stronghold Dungeon Library Access", "Runestone Shard"])

    def test_lava_lowered(self):
        self.assertNotAccessible("MagmaChamber_Center2_Middle", "MagmaChamber_Center2_Lower_16", [])
        self.assertAccessible("MagmaChamber_Center2_Middle", "MagmaChamber_Center2_Lower_16",
                              ["Magma Chamber Lowered Lava"])


class MagmaChamberMinimumLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_mozzie_room_accessible_with_no_keys(self):
        self.assertAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked", [])

    def test_alchemist_lab_locked_door(self):
        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked", [])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber key"])

        self.assertNotAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                                 ["Magma Chamber Mozzie Room Unlocked", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber Mozzie Room Unlocked", "Magma Chamber key", "Magma Chamber key"])
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked",
                              ["Magma Chamber Alchemist Lab Unlocked"])


class MagmaChamberNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_mozzie_room_accessible_with_no_keys(self):
        self.assertAccessible("MagmaChamber_Center9_Middle", "magma_chamber_mozzie_room_unlocked", [])

    def test_alchemist_lab_accessible_with_no_keys(self):
        self.assertAccessible("MagmaChamber_AlchemistLab_West", "magma_chamber_alchemist_lab_unlocked", [])


class MagmaChamberPlotlessTests(TestArea):
    options = {
        "skip_plot": 1
    }

    def test_runestone_accessible(self):
        self.assertNotAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava", [])
        self.assertAccessible("MagmaChamber_Runestone", "magma_chamber_lower_lava",["Runestone Shard"])
