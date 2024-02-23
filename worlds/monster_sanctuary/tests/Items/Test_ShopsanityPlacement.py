from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestShopsanityItemPlacement(MonsterSanctuaryTestBase):
    options = {
        "shopsanity": 1
    }

    def test_currency_cannot_be_in_shops(self):
        self.assert_item_can_not_be_placed(
            "100 G",
            "MountainPath_Center3_TreasureHunter_1")

    def test_multi_items_cannot_be_in_shops(self):
        self.assert_item_can_not_be_placed(
            "2x Iron",
            "MountainPath_Center3_TreasureHunter_1")

    def test_keys_must_be_in_limited_shops(self):
        self.assert_item_can_not_be_placed(
            "Mountain Path key",
            "MountainPath_Center3_TreasureHunter_1")

        self.assert_item_can_be_placed(
            "Mountain Path key",
            "MagmaChamber_GoblinTrader_GoblinTrader_1")

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
