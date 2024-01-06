from typing import List

from test.TestBase import TestBase
from worlds.monster_sanctuary import items, locations, MonsterSanctuaryItem, MonsterSanctuaryItemCategory
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestItems(MonsterSanctuaryTestBase):
    def test_all_default_items_exist(self):
        for location_name in locations.location_data:
            data = locations.location_data[location_name]
            item = items.item_data.get(data.default_item)
            if item is None:
                print(f"{data.default_item} was not found")
            self.assertIsNot(item, None)

    def test_get_item_type(self):
        self.assertTrue(items.is_item_type("Champion Defeated", MonsterSanctuaryItemCategory.RANK))
        self.assertFalse(items.is_item_type("Feather",
                                            MonsterSanctuaryItemCategory.RANK,
                                            MonsterSanctuaryItemCategory.MONSTER,
                                            MonsterSanctuaryItemCategory.FLAG))

    def test_key_items_appear_correct_number_of_times(self):
        key_items = [items.item_data[item_name] for item_name in items.item_data
                     if items.item_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM]
        for key_item in key_items:
            item_pool_items = [item for item in self.multiworld.itempool
                               if item.name == key_item.name]
            self.assertEqual(key_item.count, len(item_pool_items), key_item.name)


class TestDefaultItemProbability(MonsterSanctuaryTestBase):
    def test_default_probability(self):
        self.assertEqual(len(items.item_drop_probabilities), 354)

    def test_no_key_items_generate(self):
        itempool: List[MonsterSanctuaryItem] = []
        item_exclusions = ["Multiple"]
        for i in range(1000):
            item_name = items.get_random_item_name(self.multiworld.worlds[1], itempool, group_exclude=item_exclusions)
            item = items.MonsterSanctuaryItem(self.player, item_name, items.item_data[item_name])
            itempool.append(item)

        key_items = [item for item in itempool if items.item_data[item.name] == MonsterSanctuaryItemCategory.KEYITEM]
        self.assertEqual(0, len(key_items))
        rank_items = [item for item in itempool if items.item_data[item.name] == MonsterSanctuaryItemCategory.RANK]
        self.assertEqual(0, len(rank_items))
        flag_items = [item for item in itempool if items.item_data[item.name] == MonsterSanctuaryItemCategory.FLAG]
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

