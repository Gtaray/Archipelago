from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class KeeperStrongholdTests(TestArea):
    def test_dungeon_is_accessible(self):
        self.starting_regions = ["KeeperStronghold_EastStairwell"]
        self.run_tests([
            ["StrongholdDungeon_Jail_5", False, []],
            ["StrongholdDungeon_Jail_5", True, ["Champion Defeated", "Champion Defeated", "Champion Defeated"]],
        ])
