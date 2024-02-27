from typing import List, Dict

from test.bases import WorldTestBase
from worlds.monster_sanctuary import encounters as ENCOUNTERS
from worlds.monster_sanctuary import locations as LOCATIONS


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

    def test_all_monsters_are_accessible(self):
        monsters = {}

        # Get a list of all monsters that can be found in encounters
        for encounter_name, encounter_data in self.world.encounters.items():
            # if the goal is to defeat the mad lord, then we don't include that location
            if (self.multiworld.worlds[1].options.goal == "defeat_mad_lord"
                    and encounter_name == "AbandonedTower_Final_1"):
                continue

            i = 0
            for monster in encounter_data.monsters:
                location = self.multiworld.get_location(f"{encounter_name}_{i}", self.player)
                if location is None:
                    continue
                monsters[location.item.name] = True
                i += 1

        # Now go through all item locations and get any eggs that have been placed
        eggs = [egg.name for egg in self.multiworld.itempool if egg.name.endswith(" Egg")]
        for egg in eggs:
            monster_name = egg.replace(" Egg", "")
            if monster_name == "???":
                monster_name = "Plague Egg"

            monsters[monster_name] = True

        for monster_name in ENCOUNTERS.monster_data:
            with self.subTest(f"{monster_name} can be found"):
                self.assertIn(monster_name, monsters)


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


class TestMonsterRandomizerOn(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 1
    }

    def test_all_monsters_available(self):
        monster_counts: Dict[str, int] = {name: 0 for name in ENCOUNTERS.monster_data}

        for name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                monster_counts[monster.name] += 1

        for name, count in monster_counts.items():
            # We don't randomize these
            if name in ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]:
                continue

            with self.subTest("Monster has been placed", name=name, count=count):
                self.assertGreaterEqual(count, 1)

    def test_monster_eggs_in_item_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]

        with self.subTest("Koi Egg is in item pool"):
            self.assertIn("Koi Egg", item_names)

        with self.subTest("Bard Egg is in item pool"):
            self.assertIn("Bard Egg", item_names)


class TestMonsterRandomizerShuffle(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 2
    }

    def test_monsters_are_where_they_are_supposed_to_be(self):
        """Ensures that all monster locations contain the correct monster based on the shuffle logic"""
        for encounter_name, encounter in ENCOUNTERS.encounter_data.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter_name}_{i}"
                location = self.multiworld.get_location(location_name, 1)
                expected = self.multiworld.worlds[1].species_swap[encounter.monsters[i].name]

                with self.subTest(f"Monster should be {expected.name}",
                                  actual=location.item.name,
                                  location_name=location_name):
                    self.assertEqual(expected.name, location.item.name)

    def test_all_monsters_shuffled(self):
        for name, monster in ENCOUNTERS.monster_data.items():
            with self.subTest("Should be shuffled", name=name):
                self.assertIn(name, self.multiworld.worlds[1].species_swap)
                print(f"{name} -> {self.multiworld.worlds[1].species_swap[name]}")

    def test_monsters_only_appear_once(self):
        swapped_names = [monster.name for name, monster in self.multiworld.worlds[1].species_swap.items()]
        for name, monster in ENCOUNTERS.monster_data.items():
            with self.subTest("Should only show up once", name=name):
                self.assertEqual(1, swapped_names.count(name))

    def test_monster_eggs_in_item_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]

        def test_egg_is_in_item_pool(monster_name):
            monster = self.multiworld.worlds[1].species_swap[monster_name]
            with self.subTest("Egg is in item pool", monster=monster.name):
                self.assertIn(monster.egg_name(), item_names)

        test_egg_is_in_item_pool("Mad Lord")
        test_egg_is_in_item_pool("Plague Egg")
        test_egg_is_in_item_pool("Tanuki")
        test_egg_is_in_item_pool("Sizzle Knight")
        test_egg_is_in_item_pool("Ninki")

    def test_shuffled_tanuki_is_available(self):
        monster = self.multiworld.worlds[1].species_swap["Tanuki"]
        location = self.multiworld.get_location("Menu_0_0", self.player)
        self.assertEqual(location.item.name, monster.name)


class TestMonsterRandomizerEncounter(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 3
    }

    def test_all_monsters_available(self):
        monster_counts: Dict[str, int] = {name: 0 for name in ENCOUNTERS.monster_data}

        for name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                monster_counts[monster.name] += 1

        for name, count in monster_counts.items():
            # We don't randomize these
            if name in ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]:
                continue

            with self.subTest("Monster has been placed", name=name, count=count):
                self.assertGreaterEqual(count, 1)
