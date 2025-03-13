import unittest

from BaseClasses import ItemClassification
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestBardEggLocation_Vanilla(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "spectral_familiar_egg_placement": 0
    }

    def test_items_are_vanilla(self):
        with self.subTest("Spectral Wolf Egg Check is Vanilla"):
            self.assert_item_is_at_location("Eternity's End - Spectral Wolf", "Spectral Wolf Egg")

        with self.subTest("Spectral Eagle Egg Check is Vanilla"):
            self.assert_item_is_at_location("Eternity's End - Spectral Eagle", "Spectral Eagle Egg")

        with self.subTest("Spectral Toad Egg Check is Vanilla"):
            self.assert_item_is_at_location("Eternity's End - Spectral Toad", "Spectral Toad Egg")

        with self.subTest("Spectral Lion Egg Check is Vanilla"):
            self.assert_item_is_at_location("Eternity's End - Spectral Lion", "Spectral Lion Egg")
