from typing import List

from test.bases import WorldTestBase
from worlds.monster_sanctuary import encounters as ENCOUNTERS


class TestMonsterRandomizerBase(WorldTestBase):
    game = "Monster Sanctuary"
    player: int = 1

    def test_all_monster_locations_exist(self):
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter_name}_{i}"

                with self.subTest("Location should exist", location_name=location_name):
                    location = self.multiworld.get_location(location_name, 1)
                    self.assertIsNotNone(location)

    def test_special_monsters_are_not_placed(self):
        special_monsters = ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                with self.subTest("Monster is not a special monster", monster=monster.name):
                    self.assertTrue(monster not in special_monsters)

    def test_no_monsters_placed_where_they_should_not_be(self):
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                with self.subTest("Monster is not placed where it shouldn't be", monster=monster.name):
                    self.assertTrue(monster not in encounter.monster_exclusions)

    def test_required_monsters_are_placed(self):
        def test_monsters(msg: str, abilities: List[str]):
            with self.subTest(msg):
                found: bool = False
                for monster in monsters:
                    if set(abilities) & set(monster.groups):
                        found = True
                        break
                self.assertTrue(found)

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave")]
        test_monsters("Breakable Walls shows up in Mountain Path or Blue Caves", ["Breakable Walls"])
        test_monsters("Flying shows up in Mountain Path or Blue Caves", ["Flying"])

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace")]
        test_monsters("Mount shows up before Magma Chamber",
                      ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"])

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods")]
        test_monsters("Water Orb shows up before Horizon Beach", ["Water Orbs"])
        test_monsters("Fire Orb shows up before Horizon Beach", ["Fire Orbs"])
        test_monsters("Lightning Orb shows up before Horizon Beach", ["Lightning Orbs"])
        test_monsters("Earth Orb shows up before Horizon Beach", ["Earth Orbs"])


class TestMonsterRandomizerOff(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 0
    }

    def test_monsters_are_not_randomized(self):
        for encounter_name, encounter in ENCOUNTERS.encounter_data.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter.name}_{i}"
                location = self.multiworld.get_location(location_name, 1)

                with self.subTest("Monsters should match", name=encounter.monsters[i].name):
                    self.assertIsNotNone(location)
                    self.assertEqual(location.item.name, encounter.monsters[i].name)