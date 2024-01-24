from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase
from worlds.monster_sanctuary import locations as LOCATIONS


class TestLocationNames(MonsterSanctuaryTestBase):
    def test_all_locations_have_names(self):
        for logical_name, location in LOCATIONS.location_data.items():
            with self.subTest(f"{logical_name} has readable name"):
                self.assertNotEquals(logical_name, location.name)

    def test_locations_have_unique_names(self):
        checks = [location.name for id, location in LOCATIONS.location_data.items()]
        for check in checks:
            with self.subTest(f"Checking that {check} is a unique"):
                self.assertEqual(1, checks.count(check))


