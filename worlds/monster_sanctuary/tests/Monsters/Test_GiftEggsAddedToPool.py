from test.bases import WorldTestBase
from worlds.monster_sanctuary import locations as LOCATIONS
from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizer import TestMonsterRandomizerOn, \
    TestMonsterRandomizerOff, TestMonsterRandomizerShuffle, TestMonsterRandomizerEncounter


class TestEggRandomizer(WorldTestBase):
    game = "Monster Sanctuary"
    player: int = 1


class TestEggRandomizerOn(TestEggRandomizer):
    options = {
        "add_gift_eggs_to_pool": 1,
        "randomize_monsters": 1
    }
    run_default_tests = False

    def assert_in_item_pool(self, item_name: str, count: int = 1):
        entries = [item.name for item in self.multiworld.itempool if item.name == item_name]

        with self.subTest(f"{item_name} is in item pool at least {count} times"):
            self.assertGreaterEqual(len(entries), count)

    def test_required_eggs_are_in_item_pool(self):
        world = self.multiworld.worlds[1]

        if world.options.randomize_monsters == "by_specie":
            self.assert_in_item_pool(world.species_swap["Koi"].egg_name())
            self.assert_in_item_pool(world.species_swap["Bard"].egg_name())
            self.assert_in_item_pool(world.species_swap["Skorch"].egg_name())
            self.assert_in_item_pool(world.species_swap["Shockhopper"].egg_name(), 3)
        else:
            self.assert_in_item_pool("Koi Egg")
            self.assert_in_item_pool("Bard Egg")
            self.assert_in_item_pool("Skorch Egg")
            self.assert_in_item_pool("Shockhopper Egg", 3)


class TestEggRandomizerOnWithoutRandomizedMonsters(TestEggRandomizerOn, TestMonsterRandomizerOff):
    options = {
        "add_gift_eggs_to_pool": 1,
        "randomize_monsters": 0
    }


class TestEggRandomizerOnWithShuffledMonsters(TestEggRandomizerOn, TestMonsterRandomizerShuffle):
    options = {
        "add_gift_eggs_to_pool": 1,
        "randomize_monsters": 2
    }


class TestEggRandomizerOnWithEncounterShuffledMonsters(TestEggRandomizerOn, TestMonsterRandomizerEncounter):
    options = {
        "add_gift_eggs_to_pool": 1,
        "randomize_monsters": 3
    }


class TestEggRandomizerOff(TestEggRandomizer):
    options = {
        "add_gift_eggs_to_pool": 0,
        "randomize_monsters": 1
    }
    run_default_tests = False

    def assert_location_contains_item(self, location_name, item_name):
        with self.subTest(f"{item_name} is placed at {location_name}"):
            location = self.multiworld.get_location(location_name, 1)
            self.assertEqual(location.item.name, item_name)

    def test_required_eggs_are_placed(self):
        world = self.multiworld.worlds[1]

        if world.options.randomize_monsters == "by_specie":
            self.assert_location_contains_item("Sun Palace - Caretaker 1",
                                               world.species_swap["Koi"].egg_name())
            self.assert_location_contains_item("Forgotten World - Wanderer Room",
                                               world.species_swap["Bard"].egg_name())
            self.assert_location_contains_item("Magma Chamber - Bex",
                                               world.species_swap["Skorch"].egg_name())
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Egg Reward 1",
                                               world.species_swap["Shockhopper"].egg_name())
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Light Egg Reward",
                                               world.species_swap["Shockhopper"].egg_name())
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Dark Egg Reward",
                                               world.species_swap["Shockhopper"].egg_name())

        else:
            self.assert_location_contains_item("Sun Palace - Caretaker 1", "Koi Egg")
            self.assert_location_contains_item("Forgotten World - Wanderer Room", "Bard Egg")
            self.assert_location_contains_item("Magma Chamber - Bex","Skorch Egg")
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Egg Reward 1", "Shockhopper Egg")
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Light Egg Reward", "Shockhopper Egg")
            self.assert_location_contains_item("Snowy Peaks - Cryomancer - Dark Egg Reward", "Shockhopper Egg")

