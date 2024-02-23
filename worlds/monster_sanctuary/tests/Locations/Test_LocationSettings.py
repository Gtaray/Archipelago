from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestCryomancer_NoShifts(MonsterSanctuaryTestBase):
    options = {
        "monster_shift_rule": 0
    }

    def test_cryomancer_locations_do_not_exist(self):
        with self.subTest("Cryomancer 2 doesn't exist"):
            self.assertNotIn("Snowy Peaks - Cryomancer 2", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Cryomancer 3 doesn't exist"):
            self.assertNotIn("Snowy Peaks - Cryomancer 3", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Cryomancer 4 doesn't exist"):
            self.assertNotIn("Snowy Peaks - Cryomancer 4", self.multiworld.regions.location_cache[self.player])


class TestCryomancer_WithShifts(MonsterSanctuaryTestBase):
    options = {
        "monster_shift_rule": 1
    }

    def test_cryomancer_locations_exist(self):
        with self.subTest("Snowy Peaks - Cryomancer - Light Egg Reward"):
            self.assertIn("Snowy Peaks - Cryomancer - Light Egg Reward", self.multiworld.regions.location_cache[self.player])
        with self.subTest("Snowy Peaks - Cryomancer - Dark Egg Reward"):
            self.assertIn("Snowy Peaks - Cryomancer - Dark Egg Reward", self.multiworld.regions.location_cache[self.player])


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


shops = [
    "Treasure Hunter - Small Potion",
    "Treasure Hunter - Phoenix Tear",
    "Treasure Hunter - Shell",
    "Treasure Hunter - Sustain Ring",
    "Equipment Merchant - Wand",
    "Equipment Merchant - Claws",
    "Equipment Merchant - Shuriken",
    "Equipment Merchant - Shell+1",
    "Equipment Merchant - Vital Ring+1",
    "Equipment Merchant - Belt",
    "Equipment Merchant - Feather",
    "Equipment Merchant - Hide+2",
    "Equipment Merchant - Bandana+2",
    "Equipment Merchant - Crit Ring+2",
    "Equipment Merchant - Staff+2",
    "Equipment Merchant - Morning Star+2",
    "Equipment Merchant - Bracer+2",
    "Equipment Merchant - Needle+3",
    "Equipment Merchant - Wizard Hat+3",
    "Equipment Merchant - Helmet+3",
    "Equipment Merchant - Cestus+3",
    "Equipment Merchant - Ribbon+4",
    "Equipment Merchant - Cape+4",
    "Equipment Merchant - Orb+4",
    "Equipment Merchant - Katar+4",
    "Equipment Merchant - Impact Ring+5",
    "Equipment Merchant - Diadem+5",
    "Equipment Merchant - Coat+5",
    "Equipment Merchant - Kunai+5",
    "Equipment Merchant - Claws+5",
    "Equipment Merchant - Wand+5",
    "Consumable Merchant - Small Potion",
    "Consumable Merchant - Small Antidote",
    "Consumable Merchant - Phoenix Tear",
    "Consumable Merchant - Skill Resetter",
    "Consumable Merchant - Potion",
    "Consumable Merchant - Smoke Bomb",
    "Consumable Merchant - Monster Bell",
    "Consumable Merchant - Crystal Shard",
    "Consumable Merchant - Antidote",
    "Consumable Merchant - Mass Potion",
    "Consumable Merchant - Mass Antidote",
    "Consumable Merchant - Combo Potion",
    "Consumable Merchant - Big Potion",
    "Consumable Merchant - Mega Potion",
    "Consumable Merchant - Phoenix Serum",
    "Food Merchant - Apple",
    "Food Merchant - Berry",
    "Food Merchant - Potato",
    "Food Merchant - Walnut",
    "Food Merchant - Pear",
    "Food Merchant - Grapes",
    "Food Merchant - Corn",
    "Food Merchant - Hazelnut",
    "Food Merchant - Mango",
    "Food Merchant - Carrot",
    "Food Merchant - Almond",
    "Food Merchant - Strawberry",
    "Food Merchant - Raspberry",
    "Food Merchant - Orange",
    "Food Merchant - Cookie Mushroom",
    "Traveling Merchant - Orb+2",
    "Traveling Merchant - Tome+2",
    "Traveling Merchant - Level Badge",
    "Traveling Merchant - Bow",
    "Traveling Merchant - Heavy Mace",
    "Traveling Merchant - Poisoned Dart",
    "Rhazes - Mass Potion",
    "Rhazes - Combo Potion",
    "Rhazes - Big Potion",
    "Rhazes - Skill Potion",
    "Rhazes - Cauldron",
    "Rhazes - ??? Egg",
    "Rhazes - Mega Potion",
    "Rhazes - Phoenix Serum",
    "Rhazes - Reward Box Lvl 1",
    "Rhazes - Reward Box Lvl 2",
    "Rhazes - Reward Box Lvl 3",
    "Rhazes - Reward Box Lvl 4",
    "Goblin Trader - Skill Potion",
    "Goblin Trader - Switch Stone",
    "Goblin Trader - Shift Stone",
    "Golem Merchant - Vital Ring+4",
    "Golem Merchant - Mana Ring+4",
    "Golem Merchant - Sustain Ring+4",
    "Golem Merchant - Level Badge",
    "Golem Merchant - Craft Box",
    "Golem Merchant - Thermal Reactor",
    "Golem Merchant - Charging Sphere",
    "Golem Merchant - Shield Generator"
]

class TestShopsanityLocationsDisabled(MonsterSanctuaryTestBase):
    options = {
        "shopsanity": 0
    }

    def test_shopsanity_locations_are_not_added(self):
        for shop in shops:
            self.assert_location_does_not_exist(shop)


class TestShopsanityLocationsEnabled(MonsterSanctuaryTestBase):
    options = {
        "shopsanity": 1
    }

    def test_shopsanity_locations_are_added(self):
        for shop in shops:
            self.assert_location_exists(shop)

