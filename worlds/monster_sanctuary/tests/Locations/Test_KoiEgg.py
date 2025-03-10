from BaseClasses import ItemClassification
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestKoiEggLocation_Vanilla(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "koi_egg_placement": 0
    }

    def test_items_are_vanilla(self):
        with self.subTest("Caretaker Egg Check is Koi Egg"):
            self.assert_item_is_at_location("Sun Palace - Caretaker 1", "Koi Egg")
