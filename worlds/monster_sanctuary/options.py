from Options import Toggle, Choice, Range, SpecialRange, TextChoice, DeathLink

# TODO: Other potential options
# Randomize starting monster (because right not logic doesn't care about starting monster's ability)
    # Randomize from the original starting 4
    # Randomize to any monster
# Randomize keeper's monsters
# Remove locked doors

class RandomizeMonsters(Choice):
    """Are monsters randomized?
    No: Monsters are not randomized
    Yes: All monsters are randomized to any monster
    By Specie: Randomized such that all monsters of a given specie are replaced with another specie.
    by Encounter: All monsters of the same specie within an encounter are replaced with another specie"""
    display_name = "Randomize Monsters"
    option_no = 0
    option_yes = 1
    option_by_specie = 2
    option_by_encounter = 3
    default = 1


class MatchMonsterTier(Toggle):
    """Should monsters be randomized to other monsters of roughly the same strength?
    Does nothing if monsters are not randomized"""
    display_name = "Randomized Monsters Match Strength"
    default = 0


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
    options_random = 3
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


class MinimumEggDropRate(Range):
    """Minimum egg drop rate for each monster. If value is 0, then the drop rate will be unchanged"""
    display_name = "Minimum Egg Drop Rate"
    range_start = 0
    range_end = 100
    default = 0


class RandomizeChestItems(Choice):
    """Are chest items randomized?
    No: Chest items are not randomized
    Yes: Chest items can contain any item
    By Type: Chest items are randomized to an item of the same type (equipment, consumable, food, etc.)
    By Tier: Chest items are randomized to an item of the same tier
    by Type and Tier: Chest items are randomized to an item of the same type and tier"""
    display_name = "Randomize Chest Items"
    option_no = 0
    option_yes = 1
    option_by_type = 2
    option_by_tier = 3
    option_by_type_and_tier = 4
    default = 1


class IncludeChaosRelics(Toggle):
    """Include Relics of Chaos in the random item pool"""
    display_name = "Include Relics of Chaos"
    default = 1


class Goal(Choice):
    """Goal to complete.
    Defeat Mad Lord: Defeat the Mad Lord
    Defeat Legendary Keepers: Defeat all legendary keepers"""
    display_name = "Goal"
    option_defeat_mad_lord = 0
    option_defeat_legendary_keepers = 1
    default = 0


monster_sanctuary_options = {
    "randomize_monsters": RandomizeMonsters,
    "match_monster_tier": MatchMonsterTier,
    "randomize_champions": RandomizeMonsters,
    "randomize_monster_shifts": RandomizeMonsterShifts,
    "encounter_evolved_monsters": CanEncounterEvolvedMonsters,
    "minimum_egg_drop_rate": MinimumEggDropRate,
    "randomize_chests": RandomizeChestItems,
    "include_chaos_relics": IncludeChaosRelics,
    "goal": Goal,
    "death_link": DeathLink
}