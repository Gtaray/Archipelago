from typing import List

from test.TestBase import TestBase
from worlds.monster_sanctuary import items, locations, MonsterSanctuaryItem, MonsterSanctuaryItemCategory
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

    def test_no_key_items_generate(self):
        itempool: List[MonsterSanctuaryItem] = []
        item_exclusions = ["Multiple"]
        for i in range(1000):
            item_name = items.get_random_item_name(self.multiworld.worlds[1], itempool, group_exclude=item_exclusions)
            item = items.MonsterSanctuaryItem(self.player, item_name, items.items_data[item_name])
            itempool.append(item)

        key_items = [item for item in itempool if items.items_data[item.name] == MonsterSanctuaryItemCategory.KEYITEM]
        self.assertEqual(0, len(key_items))
        rank_items = [item for item in itempool if items.items_data[item.name] == MonsterSanctuaryItemCategory.RANK]
        self.assertEqual(0, len(rank_items))
        flag_items = [item for item in itempool if items.items_data[item.name] == MonsterSanctuaryItemCategory.FLAG]
        self.assertEqual(0, len(flag_items))


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

