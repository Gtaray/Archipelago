from typing import Dict

from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from ..locations import locations_data, MonsterSanctuaryLocationCategory


# region Test Monster Rando Settings
class TestNoRandomization(MonsterSanctuaryTestBase):
    options = {
        "randomize_monsters": 0,
        "randomize_items": 0
    }

    def test_monsters_are_not_randomized(self):
        for location_name in locations_data:
            data = locations_data[location_name]

            # Only test monster locations
            if data.category != MonsterSanctuaryLocationCategory.MONSTER:
                continue

            expected = data.default_item
            actual = self.multiworld.get_location(location_name, self.player).item.name
            self.assertEqual(expected, actual)


class TestMonstersShuffled(MonsterSanctuaryTestBase):
    options = {
        "randomize_monsters": 2
    }

    def test_monsters_are_not_randomized(self):
        monster_map: Dict[str, str] = {}

        for location_name in locations_data:
            data = locations_data[location_name]

            # Only test monster locations
            if data.category != MonsterSanctuaryLocationCategory.MONSTER:
                continue

            actual = self.multiworld.get_location(location_name, self.player).item.name
            # The first time a monster shows up in a location, we add it to the dict
            # and then continue. Any further instance of that monster should be the same
            if monster_map.get(data.default_item) is None:
                monster_map[data.default_item] = actual
                continue

            self.assertEqual(monster_map[data.default_item], actual)
# endregion


# region Test Champion Rando Settings
class ChampionTestsBase(MonsterSanctuaryTestBase):
    def assert_empty_champion_slot_remain_empty(self):
        self.assertNotEqual("Empty Slot", self.multiworld.get_location("MountainPath_Center7_1_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_Center7_1_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_Center7_1_2", 1).item.name)

        self.assertNotEqual("Empty Slot", self.multiworld.get_location("MountainPath_West6_3_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_West6_3_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_West6_3_2", 1).item.name)

        self.assertNotEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom_6_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom_6_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom_6_2", 1).item.name)

        self.assertNotEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom3_1_0", 1).item.name)
        self.assertNotEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom3_1_1", 1).item.name)
        self.assertNotEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom3_1_2", 1).item.name)

        self.assertNotEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom2_1_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom2_1_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom2_1_2", 1).item.name)

        self.assertNotEqual("Empty Slot", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_0", 1).item.name)
        self.assertNotEqual("Empty Slot", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_1", 1).item.name)
        self.assertNotEqual("Empty Slot", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_2", 1).item.name)


class TestChampionsNotRandomized(ChampionTestsBase):
    options = {
        "randomize_champions": 0
    }

    def test_empty_champion_slot_remain_empty(self):
        self.assert_empty_champion_slot_remain_empty()


class TestChampionsAreDefault(ChampionTestsBase):
    options = {
        "randomize_champions": 1
    }

    def test_empty_champion_slot_remain_empty(self):
        self.assert_empty_champion_slot_remain_empty()


class TestChampionsShuffled(ChampionTestsBase):
    options = {
        "randomize_champions": 2
    }

    champions = {
        "MountainPath_Center7_1": ["Monk"],
        "MountainPath_West6_3": ["Steam Golem"],
        "BlueCave_ChampionRoom_6": ["Minitaur"],
        "BlueCave_ChampionRoom2_1": ["Specter"],
        "BlueCave_ChampionRoom3_1": ["Monk", "Ascendant", "Monk"],
        "StrongholdDungeon_SummonRoom_1": ["Azerach"],
        "StrongholdDungeon_South2_2": ["Beetloid"],
        "SnowyPeaks_ChampionRoom_7": ["Akhlut"],
        "SnowyPeaks_ChampionRoom2_0": ["Draconov", "Dracozul", "Draconov"],
        "SunPalace_North3_3": ["Kanko"],
        "SunPalace_EastChampion_2": ["Diavola"],
        "SunPalace_East6_3": ["Qilin"],
        "AncientWoods_North3_9": ["Goblin Hood", "Goblin King", "Goblin Warlock"],
        "AncientWoods_East3_1": ["Raduga"],
        "AncientWoods_SouthChampion_1": ["Brutus"],
        "HorizonBeach_EastChampion_2": ["Vodinoy"],
        "HorizonBeach_Champion_2": ["Elderjel"],
        "MagmaChamber_Champion_0": ["Asura"],
        "MagmaChamber_Champion2_6": ["Gryphonix"],
        "Underworld_WestCatacomb9_Interior_14": ["Draconoir"],
        "Underworld_West4_4": ["Spinner"],
        "MysticalWorkshop_North4_Upper_0": ["Goblin Pilot"],
        "MysticalWorkshop_Vertraag_0": ["Vertraag"],
        "BlobBurg_Champion_0": ["King Blob"],
        "ForgottenWorld_DracomerLair_1": ["Dracomer"],
        "ForgottenWorld_TerradrileLair2_4": ["Terradrile"],
        "AbandonedTower_Final_1": ["Mad Lord"],
    }

    def test_champions_are_shuffled(self):
        shuffled_champions = {}
        for location_name in self.champions:
            for i in range(3):
                loc = self.multiworld.get_location(f"{location_name}_{i}", self.player)
                if loc.item.name == "Empty Slot":
                    break

                if shuffled_champions.get(location_name) is None:
                    shuffled_champions[location_name] = []
                shuffled_champions[location_name].append(loc.item.name)

        self.assertCountEqual(self.champions, shuffled_champions)


class TestChampionsRandomized(ChampionTestsBase):
    options = {
        "randomize_champions": 3
    }

    def test_empty_champion_slot_remain_empty(self):
        self.assert_empty_champion_slot_remain_empty()
# endregion
