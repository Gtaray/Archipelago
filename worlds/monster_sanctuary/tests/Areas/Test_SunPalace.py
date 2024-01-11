from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class SunPalaceTests(TestArea):
    def test_raise_center_1(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_1", [])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_1",
                                 ["Vaero"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_1",
                              ["Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_1",
                              ["Kongamato"])

    def test_raise_center_2(self):
        # Test without the water lowered
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Koi", "Double Jump Boots"])

        # Test with the water lowered
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Sun Palace Lower Water"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Double Jump Boots"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                                 ["Kongamato"])

        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Sun Palace Lower Water", "Double Jump Boots"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_2",
                              ["Sun Palace Lower Water", "Sun Palace Lower Water", "Kongamato"])

    def test_raise_center_3(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3", [])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Koi"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Kongamato"])
        self.assertNotAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                                 ["Double Jump Boots"])

        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                              ["Koi", "Kongamato"])
        self.assertAccessible("SunPalace_Center", "sun_palace_raise_center_3",
                              ["Sun Palace Lower Water", "Sun Palace Lower Water", "Double Jump Boots"])

    def test_lower_water_1(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center"])

    def test_lower_water_2(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_lower_water_1", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_lower_water_1",
                              ["Sun Palace Raise Center", "Sun Palace Raise Center"])

    # We don't need to test if we can get to the shortcut areas normally
    # because the above tests for the raise_center flags are in the same spots
    # as the shortcuts. So if we can get to one, we can get to the other
    def test_east_shortcut(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_east_shortcut", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_east_shortcut", ["Sun Palace East Shortcut"])

    def test_west_shortcut(self):
        self.assertNotAccessible("SunPalace_Center", "sun_palace_west_shortcut", [])
        self.assertAccessible("SunPalace_Center", "sun_palace_west_shortcut", ["Sun Palace West Shortcut"])
