from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MountainPathTests(TestArea):
    def test_champion_is_accessible_with_no_items(self):
        self.assertAccessible("MountainPath_North1", "MountainPath_West6_Champion", [])

    def test_champion_required_to_access_stronghold(self):
        self.assertNotAccessible("MountainPath_North1", "KeeperStronghold_WestStairwell_5", [])
        self.assertAccessible("MountainPath_North1", "KeeperStronghold_WestStairwell_5", ["Champion Defeated"])


class MountainPathPlotlessTests(TestArea):
    options = {
        "skip_plot": 1
    }

    def test_east1_accessible(self):
        self.assertAccessible("MountainPath_North1", "KeeperStronghold_WestStairwell_5", [])
