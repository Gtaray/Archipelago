from BaseClasses import CollectionState
from worlds.monster_sanctuary import encounters as ENCOUNTERS
from worlds.monster_sanctuary.rules import can_use_ability
from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizer import TestMonsterRandomizerBase


class TestLockedExplorationAbilities_Off(TestMonsterRandomizerBase):
    def test_monsters_require_item_to_use_explore_ability(self):
        for monster_name, monster_data in ENCOUNTERS.monster_data.items():
            explore_abilities_locked = self.multiworld.worlds[1].options.lock_explore_abilities != "off"

            explore_item = None
            if self.multiworld.worlds[1].options.lock_explore_abilities == "type":
                explore_item = monster_data.explore_type_item
            elif self.multiworld.worlds[1].options.lock_explore_abilities == "ability":
                explore_item = monster_data.explore_ability_item
            if self.multiworld.worlds[1].options.lock_explore_abilities == "species":
                explore_item = monster_data.explore_species_item

            with self.subTest(f"{monster_name} requires {explore_item} to use ability"):

                # Instantiate a new collection state so each run can have its own
                state = CollectionState(self.multiworld)
                self.assertFalse(can_use_ability(monster_name, state, self.player))

                state.collect(self.multiworld.worlds[1].create_item(monster_name))
                self.assertEqual(can_use_ability(monster_name, state, self.player), not explore_abilities_locked)

                if self.multiworld.worlds[1].options.lock_explore_abilities != 0:
                    state.collect(self.multiworld.worlds[1].create_item(explore_item))
                    self.assertTrue(can_use_ability(monster_name, state, self.player))


class TestLockedExplorationAbilities_Type(TestLockedExplorationAbilities_Off):
    options = {
        "lock_explore_abilities": 1
    }


class TestLockedExplorationAbilities_Ability(TestLockedExplorationAbilities_Off):
    options = {
        "lock_explore_abilities": 2
    }


class TestLockedExplorationAbilities_Species(TestLockedExplorationAbilities_Off):
    options = {
        "lock_explore_abilities": 3
    }
