import unittest

from BaseClasses import ItemClassification
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestBardEggLocation_Vanilla(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "bard_egg_placement": 0
    }

    def test_items_are_vanilla(self):
        with self.subTest("Wanderer Egg Check is Bard Egg"):
            self.assert_item_is_at_location("Forgotten World - Wanderer Room", "Bard Egg")
