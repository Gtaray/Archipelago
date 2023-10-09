from test.TestBase import TestBase
from worlds.monster_sanctuary import items, locations
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestItems(MonsterSanctuaryTestBase):
    def test_all_default_items_exist(self):
        for location_name in locations.locations_data:
            data = locations.locations_data[location_name]
            item = items.items_data.get(data.default_item)
            if item is None:
                print(f"{data.default_item} was not found")
            self.assertIsNot(item, None)


class TestDefaultItemProbability(MonsterSanctuaryTestBase):
    def test_default_probability(self):
        self.assertEqual(len(items.item_drop_probabilities), 354)


class TestMinimumItemProbability(MonsterSanctuaryTestBase):
    options = {
        "drop_chance_craftingmaterial": 1,
        "drop_chance_consumable": 1,
        "drop_chance_food": 1,
        "drop_chance_catalyst": 1,
        "drop_chance_weapon": 1,
        "drop_chance_accessory": 1,
        "drop_chance_currency": 1,
    }

    def test_minimum_probability(self):
        self.assertEqual(71, len(items.item_drop_probabilities))


class TestMaximumItemProbability(MonsterSanctuaryTestBase):
    options = {
        "drop_chance_craftingmaterial": 100,
        "drop_chance_consumable": 100,
        "drop_chance_food": 100,
        "drop_chance_catalyst": 100,
        "drop_chance_weapon": 100,
        "drop_chance_accessory": 100,
        "drop_chance_currency": 100,
    }

    def test_maximum_probability(self):
        self.assertEqual(707, len(items.item_drop_probabilities))

