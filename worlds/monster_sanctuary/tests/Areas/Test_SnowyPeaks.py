from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class SnowyPeaksTests(TestArea):
    def test_shortcuts(self):
        self.starting_regions = ["SnowyPeaks_East4_Middle"]
        self.run_tests([
            ["snowy_peaks_east4_upper_shortcut", False, []],
            ["snowy_peaks_east4_upper_shortcut", False, ["Kongamato"]],
            ["snowy_peaks_east4_upper_shortcut", True, ["Double Jump Boots"]],
            ["snowy_peaks_east4_upper_shortcut", True, ["Snowy Peaks East 4 Upper Shortcut", "Kongamato"]]
        ])

        self.starting_regions = ["SnowyPeaks_EastMountain3_Middle"]
        self.run_tests([
            ["snowy_peaks_east_mountain_3_shortcut", False, []],
            ["snowy_peaks_east_mountain_3_shortcut", False, ["Kongamato"]],
            ["snowy_peaks_east_mountain_3_shortcut", False, ["Double Jump Boots"]],
            ["snowy_peaks_east_mountain_3_shortcut", True, ["Snowy Peaks East Mountain 3 Shortcut",
                                                            "Double Jump Boots"]],
            ["snowy_peaks_east_mountain_3_shortcut", True, ["Snowy Peaks East Mountain 3 Shortcut", "Kongamato"]]
        ])

        self.starting_regions = ["SnowyPeaks_SunPalaceEntrance"]
        self.run_tests([
            ["snowy_peaks_sun_palace_entrance_shortcut", False, []],
            ["snowy_peaks_sun_palace_entrance_shortcut", True, ["Warm Underwear"]]
        ])

    def test_progression(self):
        self.starting_regions = ["SnowyPeaks_ClothesmakerHouse"]
        self.run_tests([
            ["SnowyPeaks_ClothesmakerHouse_17700033", False, []],
            ["SnowyPeaks_ClothesmakerHouse_17700033", True, ["Raw Hide"]]
        ])
