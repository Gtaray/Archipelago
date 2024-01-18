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


class ImprovedMobilityLimitation(Toggle):
    """Limit monsters with improved mobility abilities from showing up too early.
    Abilities include: improved flying, lofty mount, improved swimming, and dual mobility

    If enabled, monsters with improved mobility abilities will not show up in the Mountain Path, Blue Caves, Stronghold Dungeon, Snowy Peaks, Sun Palace, or Ancient Woods.
    if disabled, monsters with improved mobility abilities can appear anywhere."""
    display_name = "Limit Improved Mobility Abilities"
    default = True


class LocalAreaKeys(Toggle):
    """Localized Area Keys

    If enabled, area keys will only appear in the Monster Sanctuary player's world, and they will only appear in their own area.
    If disabled, keys can appear in any world, and may be found outside their area in which they are used."""
    display_name = "Local Area Keys"
    default = False


class RemoveLockedDoors(Choice):
    """Remove Locked Doors

    No: Locked doors are not removed
    Minimal: Superfluous locked doors are removed, while ones that gate large numbers of checks remain
    All: All locked doors are removed"""
    display_name = "Remove Locked Doors"
    option_no = 0
    option_minimal = 1
    option_all = 2
    default = 1


class AddGiftEggsToPool(Toggle):
    """If enabled, any monsters you receive through gifts will have their eggs added to the item pool and their location will be randomized.

    If disabled then gift monsters are received in their normal locations.
    If monster randomization is set to shuffle, then the eggs you receive will be included in the shuffle.
    Gift monsters are: Koi, Skorch, Shockhopper, and Bard"""
    display_name = "Add Gift Monster Eggs to Item Pool"
    default = True


class MonstersAlwaysDropEggs(Toggle):
    """If enabled, monsters will always drop an egg."""
    display_name = "Monsters always drop eggs"
    default = True


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
    default = True


class ExpMultiplier(Range):
    """Modifier for experience gained. When specifying a number, XP is multiplied by this amount"""
    display_name = "Experience Multiplier"
    range_start = 1
    range_end = 5
    default = 1


class SkipIntro(Toggle):
    """Skip the intro cut scenes and tutorial dialog when starting a new file."""
    display_name = "Skip Intro Cutscenes"
    default = False


class SkipPlot(Toggle):
    """Skip plot related events and open up all areas gated by story progression."""
    display_name = "Skip Plot Requirements"
    default = False


class Goal(Choice):
    """Goal to complete.

    Defeat Mad Lord: Defeat the Mad Lord
    Defeat All Champions: Defeat all 27 Champions"""
    display_name = "Goal"
    option_defeat_mad_lord = 0
    option_defeat_all_champions = 1
    default = 0


@dataclass
class MonsterSanctuaryOptions(PerGameCommonOptions):
    randomize_monsters: RandomizeMonsters
    monster_shift_rule: RandomizeMonsterShifts
    improved_mobility_limit: ImprovedMobilityLimitation
    remove_locked_doors: RemoveLockedDoors
    local_area_keys: LocalAreaKeys
    add_gift_eggs_to_pool: AddGiftEggsToPool
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
    goal: Goal
    death_link: DeathLink
