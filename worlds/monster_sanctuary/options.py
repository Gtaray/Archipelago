from Options import Toggle, Choice, Range, DeathLink

# TODO: Other potential options
# Randomize starting monster (because right not logic doesn't care about starting monster's ability)
#   Randomize from the original starting 4
#   Randomize to any monster
# Randomize keeper's monsters
# Remove locked doors
# Randomize shops


class RandomizeMonsters(Choice):
    """Are monsters randomized?

    No: Monsters are not randomized
    Any: All monsters are randomized to any monster
    By Specie: All monsters of a given specie are randomized to the same specie.
    by Encounter: All monsters of the same specie within an encounter are randomized to the same specie"""
    display_name = "Randomize Monsters"
    option_no = 0
    option_any = 1
    option_by_specie = 2
    option_by_encounter = 3
    default = 1


class RandomizeChampions(Choice):
    """Randomize champions

    No: Champions will not be randomized
    Default: Champions will be randomized according to the Randomize Monsters game option
    Shuffle: Champions will be shuffled around
    Any: Champions will be completely randomized ignoring restrictions on the rest of the monster pool"""
    display_name = "Randomize Champions"
    option_no = 0
    option_default = 1
    option_shuffle = 2
    option_any = 3
    default = 1


class RandomizeMonsterShifts(Choice):
    """When do shifted monsters start appearing?

    Never: Shifted monsters will never appear in the wild
    After Sun Palace: Shifted monsters will start appearing after completing the Sun Palace storyline
    Any Time: Shifted monsters can appear any time"""
    display_name = "Randomize Shifted Monsters"
    option_never = 0
    option_after_sun_palace = 1
    option_any_time = 2
    default = 1


class CanEncounterEvolvedMonsters(Toggle):
    """Can evolved monsters be encountered in the wild"""
    display_name = "Evolved Monsters in the Wild"
    default = 1


class MonstersAlwaysDropEggs(Toggle):
    """If enabled, monsters will always drop an egg if you don't already have one.
    This is not shown in the rewards screen."""
    display_name = "Monsters always drop eggs"
    default = 1


class CraftingMaterialDropChance(Range):
    """Frequency that a random non-progression item is a crafting material

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Crafting Material Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class ConsumableDropChance(Range):
    """Frequency that a random non-progression item is a consumable

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Consumable Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class FoodDropChance(Range):
    """Frequency that a random non-progression item is a food item

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Food Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class CatalystDropChance(Range):
    """Frequency that a random non-progression item is a catalyst

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Catalyst Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class WeaponDropChance(Range):
    """Frequency that a random non-progression item is a weapon

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Weapon Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class AccessoryDropChance(Range):
    """Frequency that a random non-progression item is an accessory

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Accessory Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class GoldDropChance(Range):
    """Frequency that a random non-progression item is gold

    The higher this value is compared to the other drop chances, the more frequently it will occur.
    For example, if this value is twice the value of all other drop chances,
    then this type of item will occur twice as often as the others. If left at 0, this item type will never drop."""
    display_name = "Gold Drop Chance"
    range_start = 0
    range_end = 100
    default = 50


class IncludeChaosRelics(Toggle):
    """Include Relics of Chaos in the random item pool"""
    display_name = "Include Relics of Chaos"
    default = 1


class ExpMultiplier(Range):
    """Modifier for experience gained. When specifying a number, XP is multiplied by this amount"""
    display_name = "Experience Multiplier"
    range_start = 1
    range_end = 5
    default = 1


class Goal(Choice):
    """Goal to complete.

    Defeat Mad Lord: Defeat the Mad Lord
    Defeat All Champions: Defeat all 27 Champions"""
    display_name = "Goal"
    option_defeat_mad_lord = 0
    option_defeat_all_champions = 1
    default = 0

    def get_event_name(self) -> str:
        return {
            self.option_defeat_mad_lord: "Defeat Mad Lord",
        }[self.value]


monster_sanctuary_options = {
    "randomize_champions": RandomizeChampions,
    "randomize_monsters": RandomizeMonsters,
    "monster_shift_rule": RandomizeMonsterShifts,
    "monsters_always_drop_egg": MonstersAlwaysDropEggs,
    "drop_chance_craftingmaterial": CraftingMaterialDropChance,
    "drop_chance_consumable": ConsumableDropChance,
    "drop_chance_food": FoodDropChance,
    "drop_chance_catalyst": CatalystDropChance,
    "drop_chance_weapon": WeaponDropChance,
    "drop_chance_accessory": AccessoryDropChance,
    "drop_chance_currency": GoldDropChance,
    "include_chaos_relics": IncludeChaosRelics,
    "exp_multiplier": ExpMultiplier,
    "goal": Goal,
    "death_link": DeathLink
}
