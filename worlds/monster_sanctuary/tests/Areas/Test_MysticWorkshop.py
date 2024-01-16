from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MysticWorkshopTests(TestArea):
    options = {
        "remove_locked_doors": 1
    }

    def test_north_locked_door(self):
        self.assertNotAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked", [])
        self.assertNotAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked",
                                 ["Double Jump Boots", "Mystical Workshop key"])
        self.assertNotAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked",
                                 ["Double Jump Boots", "Mystical Workshop key", "Mystical Workshop key"])

        self.assertAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked",
                              ["Double Jump Boots", "Mystical Workshop key", "Mystical Workshop key", "Mystical Workshop key"])
        self.assertAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked",
                              ["Double Jump Boots", "Mystical Workshop North Unlocked"])

    def test_north_shortcut(self):
        self.assertNotAccessible("MysticalWorkshop_North4_Shortcut", "mystical_workshop_north_shortcut", [])
        self.assertAccessible("MysticalWorkshop_North4_Shortcut", "mystical_workshop_north_shortcut",
                              ["Mystical Workshop North Shortcut"])

    def test_can_unlock_abandoned_tower(self):
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access", [])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Double Jump Boots"])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Kongamato"])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Double Jump Boots", "Kongamato"])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Mystical Workshop key", "Mystical Workshop key", "Mystical Workshop key"])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Double Jump Boots", "Kongamato", "Mystical Workshop key"])
        self.assertNotAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                                 ["Double Jump Boots", "Kongamato", "Mystical Workshop key", "Mystical Workshop key"])

        self.assertAccessible("MysticalWorkshop_South1", "abandoned_tower_access",
                              ["Double Jump Boots", "Kongamato", "Mystical Workshop key", "Mystical Workshop key", "Mystical Workshop key"])


class MysticWorkshopNoLockedDoorsTests(TestArea):
    options = {
        "remove_locked_doors": 2
    }

    def test_north_accessible_with_no_keys(self):
        self.assertNotAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked", [])
        self.assertAccessible("MysticalWorkshop_North6", "mystical_workshop_north_unlocked", ["Double Jump Boots"])
