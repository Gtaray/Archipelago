from dataclasses import dataclass

from Options import Toggle, Choice, Range, DeathLink, PerGameCommonOptions


# TODO: Other potential options
# Randomize starting monster (because right not logic doesn't care about starting monster's ability)
#   Randomize from the original starting 4
#   Randomize to any monster
# Randomize keeper's monsters
# Remove locked doors
# Randomize shops


class RandomizeMonsters(Choice):
    """Randomize monsters

    No: Monsters are not randomized. Koi and Bard Egg locations are also not randomized
    Yes: All monsters are randomized independently
    By Specie: Monsters of the same specie are all randomized to another monster specie
    By Encounter: Within an encounter, all monsters of the same specie are randomized to another specie. Each encounter is randomized separately"""
    display_name = "Randomize Monsters"
    option_no = 0
    option_yes = 1
    option_by_specie = 2
    option_by_encounter = 3
    default = 1


class RandomizeChampions(Choice):
    """Randomize champions

    No: Champions will not be randomized
    Default: Champions will be randomized according to the Randomize Monsters game option
    Shuffle: Champions will be shuffled around
    Random: Champions will be completely randomized separate from the rest of the monster pool"""
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


class CanChampionMonstersAppearInWild(Toggle):
    """Determines whether champion monsters appear in the wild."""
    display_name = "Champions appear in wild"
    default = 1


class ImprovedMobilityLimitation(Choice):
    """Limit monsters with improved mobility abilities from showing up too early.
    Abilities include: improved flying, lofty mount, improved swimming, and dual mobility

    No: Do not limit monster placement based on their ability
    Mid-Game: Monsters with improved mobility abilities will not show up in the Mountain Path, Blue Caves, Stronghold Dungeon, or Snowy Peaks.
    Late-Game: Monsters with improved mobility abilities will only show up in the Underworld, Mystical Workshop, Forgotten World, and Abandoned Tower."""
    display_name = "Limit Improved Mobility Abilities"
    option_no = 0
    option_midgame = 1
    option_lategame = 2


class MonstersAlwaysDropEggs(Toggle):
    """If enabled, monsters will always drop an egg."""
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


class SkipIntro(Toggle):
    """Skip the intro cut scenes and tutorial dialog when starting a new file."""
    display_name = "Skip Intro Cutscenes"
    default = 0


class SkipPlot(Toggle):
    """Skip plot related events and open up all areas gated by story progression."""
    display_name = "Skip Plot Requirements"
    default = 0


class SkipKeeperBattles(Toggle):
    """Disable and skip all keeper battles.
    Some item checks are acquired by defeating keepers, and this will disable those checks."""
    display_name = "Skip Keeper Battles"
    default = 0


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


@dataclass
class MonsterSanctuaryOptions(PerGameCommonOptions):
    randomize_monsters: RandomizeMonsters
    # randomize_champions: RandomizeChampions
    monster_shift_rule: RandomizeMonsterShifts
    # champions_in_wild: CanChampionMonstersAppearInWild
    # evolutions_in_wild: CanEncounterEvolvedMonsters
    improved_mobility_limit: ImprovedMobilityLimitation
    monsters_always_drop_egg: MonstersAlwaysDropEggs
    drop_chance_craftingmaterial: CraftingMaterialDropChance
    drop_chance_consumable: ConsumableDropChance
    drop_chance_food: FoodDropChance
    drop_chance_catalyst: CatalystDropChance
    drop_chance_weapon: WeaponDropChance
    drop_chance_accessory: AccessoryDropChance
    drop_chance_currency: GoldDropChance
    include_chaos_relics: IncludeChaosRelics
    exp_multiplier: ExpMultiplier
    skip_intro: SkipIntro
    skip_plot: SkipPlot
    skip_battles: SkipKeeperBattles
    goal: Goal
    death_link: DeathLink
