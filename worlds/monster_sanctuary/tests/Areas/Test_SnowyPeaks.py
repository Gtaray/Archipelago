from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class SnowyPeaksTests(TestArea):
    def test_east_upper_shortcut(self):
        self.assertNotAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut", [])
        self.assertNotAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut",
                                 ["Kongamato"])
        self.assertAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut",
                              ["Double Jump Boots"])
        self.assertAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut",
                              ["Snowy Peaks East 4 Upper Shortcut", "Kongamato"])

    def test_east_mountain_shortcut(self):
        self.assertNotAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                                 [])
        self.assertNotAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                                 ["Kongamato"])
        self.assertNotAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                                 ["Double Jump Boots"])
        self.assertAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                              ["Snowy Peaks East Mountain 3 Shortcut", "Double Jump Boots"])
        self.assertAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                              ["Snowy Peaks East Mountain 3 Shortcut", "Kongamato"])

    def test_sun_palace_entrance_shortcut(self):
        self.assertNotAccessible("SnowyPeaks_SunPalaceEntrance", "snowy_peaks_sun_palace_entrance_shortcut",
                                 [])
        self.assertAccessible("SnowyPeaks_SunPalaceEntrance", "snowy_peaks_sun_palace_entrance_shortcut",
                              ["Warm Underwear"])

    def test_clothesmaker(self):
        self.assertNotAccessible("SnowyPeaks_ClothesmakerHouse", "SnowyPeaks_ClothesmakerHouse_17700033",
                                 [])
        self.assertAccessible("SnowyPeaks_ClothesmakerHouse", "SnowyPeaks_ClothesmakerHouse_17700033",
                              ["Raw Hide"])

    def test_cryomancer(self):
        self.assertNotAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900062", [])
        self.assertAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900062", ["Dodo"])
        self.assertAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900062", ["Dodo Egg"])

        self.assertNotAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065", [])
        self.assertNotAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065", ["Dodo"])
        self.assertNotAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065", ["Dodo Egg"])
        self.assertNotAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065",
                                 ["Sun Palace Raise Center", "Sun Palace Raise Center", "Sun Palace Raise Center"])
        self.assertAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065",
                              ["Dodo", "Sun Palace Raise Center", "Sun Palace Raise Center",
                               "Sun Palace Raise Center"])

        self.assertAccessible("SnowyPeaks_Cryomancer", "SnowyPeaks_Cryomancer_17900065",
                              ["Dodo Egg", "Sun Palace Raise Center", "Sun Palace Raise Center",
                               "Sun Palace Raise Center"])


class SnowyPeaksWithOpenShortcuts(TestArea):
    options = {
        "open_shortcuts": 1
    }

    def test_east_upper_shortcut(self):
        self.assertAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut",
                              ["Double Jump Boots"])
        self.assertAccessible("SnowyPeaks_East4_Middle", "snowy_peaks_east4_upper_shortcut",
                              ["Kongamato"])

    def test_east_mountain_shortcut(self):
        self.assertAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                              ["Double Jump Boots"])
        self.assertAccessible("SnowyPeaks_EastMountain3_Middle", "snowy_peaks_east_mountain_3_shortcut",
                              ["Kongamato"])

    def test_sun_palace_entrance_shortcut(self):
        self.assertAccessible("SnowyPeaks_SunPalaceEntrance",
                              "snowy_peaks_sun_palace_entrance_shortcut",
                              [])
