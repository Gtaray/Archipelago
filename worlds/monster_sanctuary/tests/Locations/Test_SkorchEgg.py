from BaseClasses import ItemClassification
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestSkorchEggLocation_Vanilla(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "skorch_egg_placement": 0
    }

    def test_items_are_vanilla(self):
        with self.subTest("Skorch Egg Check is Skorch Egg"):
            self.assert_item_is_at_location("Magma Chamber - Bex", "Skorch Egg")
