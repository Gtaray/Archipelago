from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class MountainPathTests(TestArea):
    def test_champion_is_accessible(self):
        self.starting_regions = ["MountainPath_North1"]
        self.run_tests([
            ["MountainPath_West6_Champion", True, []],
            ["KeeperStronghold_WestStairwell_5", False, []],
            ["KeeperStronghold_WestStairwell_5", True, ["Champion Defeated"]],
        ])
