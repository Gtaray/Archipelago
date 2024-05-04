from BaseClasses import CollectionState
from worlds.monster_sanctuary import encounters as ENCOUNTERS
from worlds.monster_sanctuary.rules import can_use_ability
from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizer import TestMonsterRandomizerBase


class TestAllMonstersHaveProgressionData(TestMonsterRandomizerBase):
    def assert_monster_has_progressive_data(self, monster):
        with self.subTest(f"{monster.name} has progressive explore item data"):
            self.assertIsNotNone(monster.explore_progression_item)
            self.assertIsNotNone(monster.explore_progression_item.item)
            self.assertGreater(monster.explore_progression_item.quantity, 0)

    def test_monsters_have_progression_data(self):
        for monster_name, monster_data in ENCOUNTERS.monster_data.items():
            self.assert_monster_has_progressive_data(monster_data)


class TestLockedExplorationAbilities_Off(TestMonsterRandomizerBase):
    def assert_ability_is_usable(self, monster_name: str):
        with self.subTest(f"{monster_name}'s ability is usable"):
            state = CollectionState(self.multiworld)
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertTrue(can_use_ability(monster_name, state, self.player))

    def assert_explore_item_is_required(self, monster_name: str, explore_item: str):
        with self.subTest(f"{monster_name} requires {explore_item} to use ability"):
            # Instantiate a new collection state so each run can have its own
            state = CollectionState(self.multiworld)
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            if self.multiworld.worlds[1].options.lock_explore_abilities != 0:
                state.collect(self.multiworld.worlds[1].create_item(explore_item))
                self.assertTrue(can_use_ability(monster_name, state, self.player))

    def assert_explore_progression_is_required(self, monster_name: str, explore_item: str, quantity: int):
        with self.subTest(f"{monster_name} requires {explore_item} {quantity} to use ability"):
            # Instantiate a new collection state so each run can have its own
            state = CollectionState(self.multiworld)
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            # +1 here because we want to loop from 0 to the quantity, including that value
            # as when i == quantity, we should be asserting that the monster can use its ability
            for i in range(quantity + 1):
                can_use = can_use_ability(monster_name, state, self.player)
                should_be_able_to_use = i == quantity
                self.assertEqual(can_use, should_be_able_to_use)
                state.collect(self.multiworld.worlds[1].create_item(explore_item))

    def assert_explore_combo_is_required(self, monster_name: str, requirements):
        pass

    def test_monsters_require_item_to_use_explore_ability(self):
        for monster_name, monster_data in ENCOUNTERS.monster_data.items():
            if self.multiworld.worlds[1].options.lock_explore_abilities == 0:
                self.assert_ability_is_usable(monster_name)
            elif self.multiworld.worlds[1].options.lock_explore_abilities == 1:
                self.assert_explore_item_is_required(monster_name, monster_data.explore_type_item)
            elif self.multiworld.worlds[1].options.lock_explore_abilities == 2:
                self.assert_explore_item_is_required(monster_name, monster_data.explore_ability_item)
            if self.multiworld.worlds[1].options.lock_explore_abilities == 3:
                self.assert_explore_item_is_required(monster_name, monster_data.explore_species_item)
            if self.multiworld.worlds[1].options.lock_explore_abilities == 4:
                self.assert_explore_progression_is_required(monster_name,
                                                            monster_data.explore_progression_item.item,
                                                            monster_data.explore_progression_item.quantity)
            if self.multiworld.worlds[1].options.lock_explore_abilities == "combo":
                self.assert_explore_combo_is_required(monster_name, monster_data.explore_combo_item)


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


# class TestLockedExplorationAbilities_Progression(TestLockedExplorationAbilities_Off):
#     options = {
#         "lock_explore_abilities": 4
#     }
#
#
# class TestLockedExplorationAbilities_Combo(TestLockedExplorationAbilities_Off):
#     options = {
#         "lock_explore_abilities": 5
#     }
