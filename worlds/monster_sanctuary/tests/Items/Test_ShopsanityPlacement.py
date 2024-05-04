from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


area_keys = [
        "Mountain Path key",
        "Blue Cave key",
        "Stronghold Dungeon key",
        "Ancient Woods key",
        "Magma Chamber key",
        "Mystical Workshop key",
        "Underworld key"
    ]


class TestAreaKeysInShopsWithLocalPlacementEnabled(MonsterSanctuaryTestBase):
    options = {
        "shopsanity": 1,
        "local_area_keys": 1,
        "goal": 3
    }

    def test_keys_must_be_in_shop_in_their_own_area(self):
        for key in area_keys:
            for location in LOCATIONS.location_data:
                # only test shop locations
                if not LOCATIONS.is_location_shop(location):
                    continue

                location_area = location.split('_')[0]
                key_area = key.replace(" ", "")

                if LOCATIONS.is_shop_limited(location) and key_area.startswith(location_area):
                    self.assert_item_can_be_placed(key, location)
                else:
                    self.assert_item_can_not_be_placed(key, location)


class TestShopsanityItemPlacement(MonsterSanctuaryTestBase):
    # Goal is set to 3 because the Mozzie item relies on that check.
    # There is no other rule in can_item_be_placed that relies on the goal
    options = {
        "goal": 3,
        "shopsanity": 1
    }
    run_default_tests = False

    def test_currency_cannot_be_in_shops(self):
        self.assert_item_can_not_be_placed(
            "100 G",
            "MountainPath_Center3_TreasureHunter_1")

    def test_multi_items_cannot_be_in_shops(self):
        self.assert_item_can_not_be_placed(
            "2x Iron",
            "MountainPath_Center3_TreasureHunter_1")

    def test_keys_must_be_in_limited_shops(self):
        for key in area_keys:
            for location in LOCATIONS.location_data:
                # only test shop locations
                if not LOCATIONS.is_location_shop(location):
                    continue

                if LOCATIONS.is_shop_limited(location):
                    self.assert_item_can_be_placed(key, location)
                else:
                    self.assert_item_can_not_be_placed(key, location)

    def test_eggs_must_be_in_limited_shops(self):
        self.assert_item_can_not_be_placed(
            "Ornithopter Egg",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_be_placed(
            "Ornithopter Egg",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

    def test_costumes_must_be_in_limited_shops(self):
        self.assert_item_can_not_be_placed(
            "Alchemist",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_be_placed(
            "Alchemist",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

    def test_restricted_items_must_be_in_limited_shops(self):
        self.assert_item_can_not_be_placed(
            "Sanctuary Token",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_not_be_placed(
            "Rare Seashell",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_not_be_placed(
            "Mozzie",
            "MountainPath_Center3_TreasureHunter_1"
        )

        self.assert_item_can_not_be_placed(
            "Celestial Feather",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_be_placed(
            "Sanctuary Token",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

        self.assert_item_can_be_placed(
            "Rare Seashell",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

        self.assert_item_can_be_placed(
            "Celestial Feather",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

        self.assert_item_can_be_placed(
            "Mozzie",
            "MagmaChamber_GoblinTrader_GoblinTrader_1"
        )
