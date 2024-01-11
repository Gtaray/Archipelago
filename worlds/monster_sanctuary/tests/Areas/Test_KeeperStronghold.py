from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class KeeperStrongholdTests(TestArea):
    def test_dungeon_is_accessible(self):
        self.assertNotAccessible("KeeperStronghold_EastStairwell", "StrongholdDungeon_Jail_5", [])
        self.assertNotAccessible("KeeperStronghold_EastStairwell", "StrongholdDungeon_Jail_5",
                                 ["Champion Defeated", "Champion Defeated", "Champion Defeated"])
        self.assertNotAccessible("KeeperStronghold_EastStairwell", "StrongholdDungeon_Jail_5",
                                 ["Blue Caves Story Complete"])
        self.assertAccessible("KeeperStronghold_EastStairwell", "StrongholdDungeon_Jail_5",
                              ["Champion Defeated", "Champion Defeated", "Champion Defeated", "Blue Caves Story Complete"])
