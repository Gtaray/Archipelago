from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea
from worlds.monster_sanctuary.encounters import get_monster, monster_data


def get_location_name(monster_name: str):
    location_name = (monster_name
                     .replace(" ", "_")
                     .replace("'", "")
                     .lower())
    return f"eggsanity_{location_name}"


class EggsanityTests(TestArea):
    options = {
        "eggsanity": 1
    }

    def check_monster_logic(self, monster_name: str):
        location_name = get_location_name(monster_name)
        monster = get_monster(monster_name)

        self.assertNotAccessible("Menu", location_name, [])
        self.assertAccessible("Menu", location_name, [monster.egg_name(True)])
        self.assertAccessible("Menu", location_name, [monster.name])

        for evolution in monster.evolution:
            evo_monster = get_monster(evolution)

            # This specifically handles the case of King Blob
            # Because the blobs can evolve to it, but King Blob does not give access to any
            # of the blob monsters
            if evo_monster.pre_evolution is None:
                return

            self.assertAccessible("Menu", location_name, [evolution])
            self.assertAccessible("Menu", location_name, [evo_monster.egg_name()])
            self.assertNotAccessible("Menu", location_name, [evo_monster.egg_name(True)])

        if monster.is_evolved():
            self.check_evolution(monster_name)

    def check_evolution(self, monster_name: str):
        location_name = get_location_name(monster_name)
        monster = get_monster(monster_name)

        if not monster.is_evolved():
            return

        self.assertNotAccessible("Menu", location_name,
                                 ["Tree of Evolution Access", monster.pre_evolution])
        self.assertNotAccessible("Menu", location_name,
                                 ["Tree of Evolution Access", monster.catalyst])
        self.assertNotAccessible("Menu", location_name,
                                 [monster.pre_evolution, monster.catalyst])

        self.assertAccessible("Menu", location_name,
                              ["Tree of Evolution Access", monster.pre_evolution, monster.catalyst])

    def test_monster_logic(self):
        for monster_name in monster_data:
            self.check_monster_logic(monster_name)
