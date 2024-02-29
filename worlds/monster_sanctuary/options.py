from dataclasses import dataclass

from Options import Toggle, Choice, Range, DeathLink, PerGameCommonOptions


# TODO: Other potential options
# Randomize starting monster (because right not logic doesn't care about starting monster's ability)
#   Randomize from the original starting 4
#   Randomize to any monster
# Randomize keeper's monsters


class StartingFamiliar(Choice):
    """Choose your starting familiar. An invalid choice will default to Wolf"""

    display_name = "Starting Familiar"
    option_wolf = 0
    option_eagle = 1
    option_toad = 2
    option_lion = 3
    default = "random"


class RandomizeMonsters(Choice):
    """Randomize monsters

    Off: Monsters are not randomized. Koi and Bard Egg locations are also not randomized
    Any: All monsters are randomized independently
    By Specie: Monsters of the same specie are all randomized to another monster specie
    By Encounter: Within an encounter, all monsters of the same specie are randomized to another specie. Each encounter is randomized separately"""
    display_name = "Randomize Monsters"
    option_off = 0
    option_any = 1
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


class ExploreAbilitiesMustBeUnlocked(Choice):
    """If enabled, explore abilities cannot be used until a corresponding item has been collected.
    The items required to use explore abilities depend on the selected option:

    Off: Explore Abilities are always available.
    Type: Monsters are grouped into 16 different categories based on monster type. There are 16 unique items to unlock abilities for all monsters of a given type
    Ability: Each explore ability must be unlocked separately. For example, unlocking Flying will allow that ability to be used on any monster with the Flying ability
    Species: Each monster species will require a unique item to unlock its explore ability (excepting evolutions where the ability doesn't change)"""
    display_name = "Explore Abilities Must be Unlocked"
    option_off = 0
    option_type = 1
    option_ability = 2
    option_species = 3
    default = 0


class Eggsanity(Toggle):
    """Add a location for all 111 monsters that are checked when you hatch or evolve that monster."""
    display_name = "Eggsanity"
    default = False


class Shopsanity(Toggle):
    """If enabled, shop inventories are randomized"""
    display_name = "Shopsanity"
    default = False


class ShopsanityPrices(Choice):
    """ONLY WORKS IF SHOPSANITY IS ENABLED.

    Modifies the prices that shops sell items for
    Normal: Shop prices are unchanged
    Weighted: Shop prices are randomized, with the cost of progression items weighted towards the upper end of the range
    Any: Shop prices are entirely randomized"""
    display_name = "Shopsanity Prices"
    option_normal = 0
    option_weighted = 1
    option_any = 2
    default = 1


class ShopsIgnoreRank(Toggle):
    """If enabled, all shops will offer their entire stock regardless of keeper rank."""
    display_name = "Shop Ignores Rank Requirements"
    default = False


class LocalAreaKeys(Toggle):
    """Localized Area Keys

    If enabled, area keys will only appear in the Monster Sanctuary player's world, and they will only appear in their own area.
    If disabled, keys can appear in any world, and may be found outside their area in which they are used."""
    display_name = "Local Area Keys"
    default = False


class RemoveLockedDoors(Choice):
    """Remove Locked Doors

    Off: Locked doors are not removed
    Minimal: Superfluous locked doors are removed, while ones that gate large numbers of checks remain
    All: All locked doors are removed"""
    display_name = "Remove Locked Doors"
    option_off = 0
    option_minimal = 1
    option_all = 2
    default = 0


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


class StartWithSmokeBombs(Toggle):
    """If enabled, the player will start with 50 Smoke Bombs."""
    display_name = "Start with 50 Smoke Bombs"
    default = True


class StartingGold(Range):
    """Override the player's starting gold, counted in increments of 100"""
    display_name = "Starting Gold (counted in increments of 100)"
    range_start = 0
    range_end = 1000
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


class ReplaceFillerWithLevelBadges(Range):
    """Replaces a percentage of filler items with Level 42 Badges, to reduce the grind required to reach endgame.
    The value is a percentage range from 0 (no filler items are replaced with level 42 badges) to 100 (all filler items are replaced with level 42 badges)"""
    display_name = "Replace Filler with Level Badges"
    range_start = 0
    range_end = 100
    default = 0


class IncludeChaosRelics(Choice):
    """Include Relics of Chaos in the random item pool

    Off: Relics of Chaos will not show up
    On: Relics of Chaos can be added to the item pool, but are not guaranteed
    Some: At least 5 Relics of Chaos will be included in the item pool
    All: All Relics of Chaos will be added to the item pool"""
    display_name = "Include Relics of Chaos"
    option_off = 0
    option_on = 1
    option_some = 2
    option_all = 3
    default = 1


class ExpMultiplier(Range):
    """Modifier for experience gained. When specifying a number, XP is multiplied by this amount"""
    display_name = "Experience Multiplier"
    range_start = 1
    range_end = 5
    default = 1


class SkipPlot(Toggle):
    """Skip plot related events and open up all areas gated by story progression."""
    display_name = "Skip Plot Requirements"
    default = False


class AddHints(Toggle):
    """Adds hints for common checks, items, and monsters"""
    display_name = "Add Hints"
    default = True


class Goal(Choice):
    """Goal to complete.

    Defeat Mad Lord: Defeat the Mad Lord
    Defeat All Champions: Defeat all 27 Champions"""
    display_name = "Goal"
    option_defeat_mad_lord = 0
    option_defeat_all_champions = 1
    option_complete_monster_journal = 2
    default = 0


@dataclass
class MonsterSanctuaryOptions(PerGameCommonOptions):
    starting_familiar: StartingFamiliar
    randomize_monsters: RandomizeMonsters
    monster_shift_rule: RandomizeMonsterShifts
    improved_mobility_limit: ImprovedMobilityLimitation
    lock_explore_abilities: ExploreAbilitiesMustBeUnlocked
    eggsanity: Eggsanity
    shopsanity: Shopsanity
    shopsanity_prices: ShopsanityPrices
    shops_ignore_rank: ShopsIgnoreRank
    remove_locked_doors: RemoveLockedDoors
    local_area_keys: LocalAreaKeys
    add_gift_eggs_to_pool: AddGiftEggsToPool
    add_smoke_bombs: StartWithSmokeBombs
    starting_gold: StartingGold
    monsters_always_drop_egg: MonstersAlwaysDropEggs
    drop_chance_craftingmaterial: CraftingMaterialDropChance
    drop_chance_consumable: ConsumableDropChance
    drop_chance_food: FoodDropChance
    drop_chance_catalyst: CatalystDropChance
    drop_chance_weapon: WeaponDropChance
    drop_chance_accessory: AccessoryDropChance
    drop_chance_currency: GoldDropChance
    replace_filler_with_level_badges: ReplaceFillerWithLevelBadges
    include_chaos_relics: IncludeChaosRelics
    exp_multiplier: ExpMultiplier
    skip_plot: SkipPlot
    hints: AddHints
    goal: Goal
    death_link: DeathLink
