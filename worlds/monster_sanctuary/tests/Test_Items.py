from worlds.monster_sanctuary import items, locations
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestItems(MonsterSanctuaryTestBase):
    def test_special_monsters_are_not_added(self):
        monsters = items.get_monsters()
        special_mons = ["Empty Slot", "Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]

        # Asserts that there are no monsters in the monster list that match the above listed special mons
        self.assertFalse(set(monsters.keys()) & set(special_mons))

    def test_all_default_items_exist(self):
        for location_name in locations.locations_data:
            data = locations.locations_data[location_name]
            item = items.items_data.get(data.default_item)
            if item is None:
                print(f"{data.default_item} was not found")
            self.assertIsNot(item, None)

