from worlds.generic.Rules import add_item_rule, add_rule, location_item_name
from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance, CollectionState


def set_rules(world: MultiWorld, player: int):
    # Defines rules for whether a location can have an item placed in it
    # Likely pulled from settings to determine what locations to use
    item_rules = { }

    # Go through each location in the world and set whether it should be used or not
    # for location in world.get_locations(player):
        # if location.name in item_rules:
            # add_item_rule(location, item_rules[location.name])

    # Defines requirements to access locations
    access_rules = {
        # Mountain Path
        "MountainPath_North3_5": lambda state: breakable_walls(state, player),
        "MountainPath_North3_3": lambda state: (has_double_jump(state, player)
                                                or distant_ledges(state, player)),
        "MountainPath_Center1_5": lambda state: (has_double_jump(state, player)
                                                 or distant_ledges(state, player)
                                                 or summon_big_rock(state, player)),
        "MountainPath_Center3_8": lambda state: impassible_vines(state, player),
        "MountainPath_Center3_9": lambda state: impassible_vines(state, player),
        "MountainPath_Center4_4": lambda state: breakable_walls(state, player),
        "MountainPath_Center5_6": lambda state: impassible_vines(state, player),
        "MountainPath_Center5_13": lambda state: magic_walls(state, player),
        "MountainPath_West4_6": lambda state: has_double_jump(state, player),
        "MountainPath_WestHidden2_1": lambda state: narrow_corridors(state, player),
        "MountainPath_Center6_2": lambda state: fire_orbs(state, player),
        "MountainPath_Center6_10": lambda state: water_orbs(state, player),

        # Blue Caves
        "BlueCave_Platforms_1": lambda state: (has_blue_caves_platform_control_access(state, player)
                                               or has_double_jump(state, player)
                                               or distant_ledges(state, player)),
        "BlueCave_Platforms_3": lambda state: breakable_walls(state, player),
        # TODO: Check if big or small rocks make check below possible
        "BlueCave_NorthFork_7": lambda state: (has_double_jump(state, player)
                                               or distant_ledges(state, player)),
        # TODO: This needs to be changed when region segments become a thing
        "BlueCave_NorthFork_10": lambda state: has_double_jump(state, player),
        "BlueCave_NorthFork_12": lambda state: ground_switches(state, player),
    }

    # Go through each location in the world and assign relevant rules for it
    for location in world.get_locations(player):
        if location.name in access_rules:
            add_rule(location, access_rules[location.name])


def has_blue_caves_platform_control_access(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves Platform Control Access", player)


def has_double_jump(state: CollectionState, player: int) -> bool:
    return state.has("Double Jump Boots", player, 1)


# region Keeper Rank
def keeper_rank_1(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 1)


def keeper_rank_2(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 3)


def keeper_rank_3(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 5)


def keeper_rank_4(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 7)


def keeper_rank_5(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 9)


def keeper_rank_6(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 12)


def keeper_rank_7(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 15)


def keeper_rank_8(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 19)


def keeper_rank_9(state: CollectionState, player: int) -> bool:
    return state.has("Champion Defeated", player, 1)
# endregion


# region keys
def has_mountain_path_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Mountain Path Key", player, count)


def has_blue_caves_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Blue Caves Key", player, count)


def has_dungeon_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Stronghold Dungeon Key", player, count)


def has_ancient_woods_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Ancient Woods Key", player, count)


def has_magma_chamber_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Magma Chamber Key", player, count)


def has_workshop_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Mystical Workshop Key", player, count)


def has_underworld_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Underworld Key", player, count)


def has_region_key(state: CollectionState, player: int, region: str) -> bool:
    return True
# endregion


# region Collective Explore Abilities
def breakable_walls(state: CollectionState, player: int) -> bool:
    return state.has_group("Breakable Walls", player)


def impassible_vines(state: CollectionState, player: int) -> bool:
    return state.has_group("Impassible Vines", player)


def distant_ledges(state: CollectionState, player: int) -> bool:
    return (flying(state, player)
            or improved_flying(state, player)
            or dual_mobility(state, player)
            or lofty_mount(state, player))


def ground_switches(state: CollectionState, player: int) -> bool:
    return (summon_big_rock(state, player)
            or summon_rock(state, player)
            or summon_mushroom(state, player))


# endregion


# region Monster Abilities
def summon_rock(state: CollectionState, player: int) -> bool:
    return state.has("Summon Rock", player)


def summon_mushroom(state: CollectionState, player: int) -> bool:
    return state.has("Summon Mushroom", player)


def summon_big_rock(state: CollectionState, player: int) -> bool:
    return state.has("Summon Big Rock", player)


def fire_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Flame Orbs", player)


def water_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Water Orbs", player)


def lightning_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Lightning Orbs", player)


def earth_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Earth Orbs", player)


def ice_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Ice Orbs", player)


def flying(state: CollectionState, player: int) -> bool:
    return state.has("Flying", player)


def improved_flying(state: CollectionState, player: int) -> bool:
    return state.has("Improved Flying", player)


def lofty_mount(state: CollectionState, player: int) -> bool:
    return state.has("Lofty Mount", player)


def dual_mobility(state: CollectionState, player: int) -> bool:
    return state.has("Dual Mobility", player)


def narrow_corridors(state: CollectionState, player: int) -> bool:
    return state.has("Narrow Corridors", player)


def magic_walls(state: CollectionState, player: int) -> bool:
    return state.has("Magic Walls", player)
# endregion
