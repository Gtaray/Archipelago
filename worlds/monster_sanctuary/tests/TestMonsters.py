from typing import Dict

from worlds.monster_sanctuary import items, locations, MonsterSanctuaryLocationCategory, MonsterSanctuaryItemCategory
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestMonsters(MonsterSanctuaryTestBase):
    def test_special_monsters_are_not_added(self):
        monsters = items.get_monsters()
        special_mons = ["Empty Slot", "Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]

        # Asserts that there are no monsters in the monster list that match the above listed special mons
        self.assertFalse(set(monsters.keys()) & set(special_mons))

    def test_correct_number_of_monsters(self):
        number_of_locations = 0
        for region in self.multiworld.regions:
            for location in region.locations:
                if locations.location_data[location.name].category == MonsterSanctuaryLocationCategory.MONSTER:
                    number_of_locations += 1

        number_of_monsters = sum(items.item_data[item.name].category == MonsterSanctuaryItemCategory.MONSTER
                                 for item in self.multiworld.itempool)

        self.assertEqual(number_of_monsters, number_of_monsters)


# region Test Champion Rando Settings
class TestChampionsNotRandomized(MonsterSanctuaryTestBase):
    options = {
        "randomize_champions": 0
    }

    def test_empty_champion_slot_remain_empty(self):
        self.assertEqual("Monk", self.multiworld.get_location("MountainPath_Center7_1_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_Center7_1_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_Center7_1_2", 1).item.name)

        self.assertEqual("Steam Golem", self.multiworld.get_location("MountainPath_West6_3_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_West6_3_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("MountainPath_West6_3_2", 1).item.name)

        self.assertEqual("Minitaur", self.multiworld.get_location("BlueCave_ChampionRoom_6_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom_6_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom_6_2", 1).item.name)

        self.assertEqual("Monk", self.multiworld.get_location("BlueCave_ChampionRoom3_0_0", 1).item.name)
        self.assertEqual("Ascendant", self.multiworld.get_location("BlueCave_ChampionRoom3_0_1", 1).item.name)
        self.assertEqual("Monk", self.multiworld.get_location("BlueCave_ChampionRoom3_0_2", 1).item.name)

        self.assertEqual("Specter", self.multiworld.get_location("BlueCave_ChampionRoom2_1_0", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom2_1_1", 1).item.name)
        self.assertEqual("Empty Slot", self.multiworld.get_location("BlueCave_ChampionRoom2_1_2", 1).item.name)

        self.assertEqual("Draconov", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_0", 1).item.name)
        self.assertEqual("Dracozul", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_1", 1).item.name)
        self.assertEqual("Draconov", self.multiworld.get_location("SnowyPeaks_ChampionRoom2_0_2", 1).item.name)


class TestChampionsShuffled(MonsterSanctuaryTestBase):
    options = {
        "randomize_champions": 1
    }

    champions = {
        "MountainPath_Center7_1": ["Monk", None, None],
        "MountainPath_West6_3": ["Steam Golem", None, None],
        "BlueCave_ChampionRoom_6": ["Minitaur", None, None],
        "BlueCave_ChampionRoom2_1": ["Specter", None, None],
        "BlueCave_ChampionRoom3_0": ["Monk", "Ascendant", "Monk"],
        "StrongholdDungeon_SummonRoom_1": ["Azerach", None, None],
        "StrongholdDungeon_South2_2": ["Beetloid", None, None],
        "SnowyPeaks_ChampionRoom_7": ["Akhlut", None, None],
        "SnowyPeaks_ChampionRoom2_0": ["Draconov", "Dracozul", "Draconov"],
        "SunPalace_North3_3": ["Kanko", None, None],
        "SunPalace_EastChampion_2": ["Diavola", None, None],
        "SunPalace_East6_2": ["Qilin", None, None],
        "AncientWoods_North3_9": ["Goblin Hood", "Goblin King", "Goblin Warlock"],
        "AncientWoods_East3_1": ["Raduga", None, None],
        "AncientWoods_SouthChampion_1": ["Brutus", None, None],
        "HorizonBeach_EastChampion_2": ["Vodinoy", None, None],
        "HorizonBeach_Champion_2": ["Elderjel", None, None],
        "MagmaChamber_Champion_0": ["Asura", None, None],
        "MagmaChamber_Champion2_6": ["Gryphonix", None, None],
        "Underworld_WestCatacomb9_Interior_14": ["Draconoir", None, None],
        "Underworld_West4_4": ["Spinner", None, None],
        "MysticalWorkshop_North4_Upper_0": ["Goblin Pilot", None, None],
        "MysticalWorkshop_Vertraag_0": ["Vertraag", None, None],
        "BlobBurg_Champion_0": ["King Blob", None, None],
        "ForgottenWorld_DracomerLair_1": ["Dracomer", None, None],
        "ForgottenWorld_TerradrileLair2_4": ["Terradrile", None, None],
        "AbandonedTower_Final_1": ["Mad Lord", None, None],
    }

    def test_champions_are_shuffled(self):
        shuffled_champions = {}
        for location_name in self.champions:
            for i in range(3):
                loc = self.multiworld.get_location(f"{location_name}_{i}", self.player)

                if shuffled_champions.get(location_name) is None:
                    shuffled_champions[location_name] = []
                if loc.item is None:
                    breakpoint()
                monster_name = loc.item.name
                shuffled_champions[location_name].append(monster_name)

        self.assertCountEqual(self.champions, shuffled_champions)
# endregion
