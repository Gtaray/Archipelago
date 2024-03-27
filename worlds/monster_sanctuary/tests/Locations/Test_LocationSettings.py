from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestCryomancer_NoShifts(MonsterSanctuaryTestBase):
    options = {
        "monster_shift_rule": 0
    }

    def test_cryomancer_locations_do_not_exist(self):
        with self.subTest("Snowy Peaks - Cryomancer - Light Egg Reward"):
            self.assertNotIn("Snowy Peaks - Cryomancer - Light Egg Reward", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Snowy Peaks - Cryomancer - Dark Egg Reward"):
            self.assertNotIn("Snowy Peaks - Cryomancer - Dark Egg Reward", self.multiworld.regions.location_cache[self.player])


class TestCryomancer_WithShifts(MonsterSanctuaryTestBase):
    options = {
        "monster_shift_rule": 1
    }

    def test_cryomancer_locations_exist(self):
        with self.subTest("Snowy Peaks - Cryomancer - Light Egg Reward"):
            self.assertIn("Snowy Peaks - Cryomancer - Light Egg Reward", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Snowy Peaks - Cryomancer - Dark Egg Reward"):
            self.assertIn("Snowy Peaks - Cryomancer - Dark Egg Reward", self.multiworld.regions.location_cache[self.player])


class TestCryomancer_ShuffledEggs(MonsterSanctuaryTestBase):
    options = {
        "randomize_monsters": 2,
        "add_gift_eggs_to_pool": 0,
        "monster_shift_rule": 1
    }

    def assert_item_is_correct(self, location_name):
        expected = self.multiworld.worlds[1].species_swap["Shockhopper"].egg_name()
        with self.subTest(f"'{location_name}' contains {expected}"):
            location = self.multiworld.get_location(location_name, self.player)
            self.assertEqual(expected, location.item.name)

    def test_cryomancer_has_shuffled_eggs(self):
        self.assert_item_is_correct("Snowy Peaks - Cryomancer - Light Egg Reward")
        self.assert_item_is_correct("Snowy Peaks - Cryomancer - Dark Egg Reward")


class TestPostGame_Off(MonsterSanctuaryTestBase):
    options = {
        "goal": 0
    }

    def test_post_game_locations_do_not_exist(self):
        with self.subTest("Parents penultimate reward doesn't exist"):
            self.assertNotIn("Keeper Stronghold - Parents - Keeper Master Gift 1", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Parents final reward doesn't exist"):
            self.assertNotIn("Keeper Stronghold - Parents - Keeper Master Gift 2", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Trevisan 1 doesn't doesn't exist"):
            self.assertNotIn("Stronghold Dungeon - Trevisan 1", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Trevisan 2 doesn't doesn't exist"):
            self.assertNotIn("Stronghold Dungeon - Trevisan 2", self.multiworld.regions.location_cache[self.player])


class TestPostGame_On(MonsterSanctuaryTestBase):
    options = {
        "goal": 1
    }

    def test_post_game_locations_exist(self):
        with self.subTest("Parents penultimate reward exists"):
            self.assertIn("Keeper Stronghold - Parents - Keeper Master Gift 1", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Parents final reward exists"):
            self.assertIn("Keeper Stronghold - Parents - Keeper Master Gift 2", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Trevisan 1 doesn't exist"):
            self.assertIn("Stronghold Dungeon - Trevisan 1", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Trevisan 2 doesn't exist"):
            self.assertIn("Stronghold Dungeon - Trevisan 2", self.multiworld.regions.location_cache[self.player])

