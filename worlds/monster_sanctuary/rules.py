from worlds.generic.Rules import add_item_rule, add_rule, location_item_name
from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance, CollectionState
from typing import List, Optional
from enum import Enum


class Operation(Enum):
    NONE = 0
    OR = 1
    AND = 2,


class AccessCondition:
    function_name: Optional[str] = None

    def __init__(self, requirements: List, operation: Operation = Operation.NONE):
        self.operands: List[AccessCondition] = []
        self.operation: Operation = operation
        self.access_rule = None

        if not requirements:
            self.access_rule = lambda state, player: True
            return

        if len(requirements) == 1:
            self.function_name = requirements[0]

        # if function name was set above, then we know that this is a leaf node
        # and can set the access rule and return
        if self.function_name is not None:
            func = globals().get(self.function_name)
            if func is None:
                raise KeyError(f"Access function '{self.function_name}' is not defined")
            else:
                self.access_rule = func
            return

        # In the case of the root access condition, requirements is formatted
        # a bit differently, and we handle that here
        if len(requirements) == 2 and (requirements[0] == "AND" or requirements[0] == "OR"):
            if requirements[0] == "AND":
                self.operation = Operation.AND
            if requirements[0] == "OR":
                self.operation = Operation.OR
            # move the read head to right after the initial AND/OR
            requirements = requirements[1]

        # go through the list of requirements
        for i in range(len(requirements)):
            op = Operation.NONE

            if requirements[i] == "AND":
                op = Operation.AND
                i += 1
            elif requirements[i] == "OR":
                op = operation.OR
                i += 1

            reqs = requirements[i]
            if isinstance(reqs, str):
                reqs = [reqs]
            self.operands += [AccessCondition(reqs, op)]

    def is_leaf(self):
        return self.operation is Operation.NONE and len(self.operands) == 0

    def has_access(self, state: CollectionState, player: int) -> bool:
        # if this node has no child conditions, return its own state
        if self.is_leaf():
            return self.access_rule(state, player)

        # If there are no operands to operate on, then return true
        if not self.operands:
            return True

        # If all operands resolve to true, then return true
        return all([condition.has_access(state, player) for condition in self.operands])


# region Navigation Flags
def blue_caves_switches_access(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves Switches Access", player)


def blue_cave_champion_room_2_west_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves to Mountain Path Shortcut", player)


def stronghold_dungeon_west_4_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Stronghold Dungeon to Blue Caves Shortcut", player)


def snowy_peaks_east4_upper_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks East 4 Upper Shortcut", player)


def snowy_peaks_east_mountain_3_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks East Mountain 3 Shortcut", player)


def snowy_peaks_sun_palace_entrance_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks to Sun Palace Shortcut", player)
# endregion


# region Key Items
def double_jump(state: CollectionState, player: int) -> bool:
    return state.has("Double Jump Boots", player, 1)


def warm_underwear(state: CollectionState, player: int) -> bool:
    return state.has("Warm Underwear", player, 1)


def raw_hide(state: CollectionState, player: int) -> bool:
    return state.has("Raw hide", player)


def all_sanctuary_tokens(state: CollectionState, player: int) -> bool:
    return state.has("Sanctuary Token", player, 5)
# endregion


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


# region Area Keys. This will need some major work once I figure out how keys work
def mountain_path_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Mountain Path key", player, count)


def blue_cave_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Blue Caves key", player, count)


def dungeon_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Stronghold Dungeon key", player, count)


def ancient_woods_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Ancient Woods key", player, count)


def magma_chamber_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Magma Chamber key", player, count)


def workshop_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Mystical Workshop key", player, count)


def underworld_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Underworld key", player, count)
# endregion


# region Explore Abilities
def distant_ledges(state: CollectionState, player: int) -> bool:
    return (flying(state, player)
            or improved_flying(state, player)
            or dual_mobility(state, player)
            or lofty_mount(state, player))


def ground_switches(state: CollectionState, player: int) -> bool:
    return (summon_big_rock(state, player)
            or summon_rock(state, player)
            or summon_mushroom(state, player))


def swimming(state: CollectionState, player: int) -> bool:
    return (basic_swimming(state, player)
            or improved_swimming(state, player)
            or dual_mobility(state, player))


def tar(state: CollectionState, player: int) -> bool:
    return tar_mount(state, player) or dual_mobility(state, player)


def breakable_walls(state: CollectionState, player: int) -> bool:
    return state.has_group("Breakable Walls", player)


def impassible_vines(state: CollectionState, player: int) -> bool:
    return state.has_group("Impassible Vines", player)


def diamond_blocks(state: CollectionState, player: int) -> bool:
    return state.has_group("Diamond Blocks", player)


def fire_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Fire Orbs", player)


def water_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Water Orbs", player)


def lightning_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Lightning Orbs", player)


def earth_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Earth Orbs", player)


def ice_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Ice Orbs", player)


def summon_rock(state: CollectionState, player: int) -> bool:
    return state.has_group("Summon Rock", player)


def summon_mushroom(state: CollectionState, player: int) -> bool:
    return state.has_group("Summon Mushroom", player)


def summon_big_rock(state: CollectionState, player: int) -> bool:
    return state.has_group("Summon Big Rock", player)


def flying(state: CollectionState, player: int) -> bool:
    return state.has_group("Flying", player)


def improved_flying(state: CollectionState, player: int) -> bool:
    return state.has_group("Improved Flying", player)


def lofty_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Lofty Mount", player)


def basic_swimming(state: CollectionState, player: int) -> bool:
    return state.has_group("Swimming", player)


def improved_swimming(state: CollectionState, player: int) -> bool:
    return state.has_group("Improved Swimming", player)


def dual_mobility(state: CollectionState, player: int) -> bool:
    return state.has_group("Dual Mobility", player)


def narrow_corridors(state: CollectionState, player: int) -> bool:
    return state.has_group("Narrow Corridors", player)


def magic_walls(state: CollectionState, player: int) -> bool:
    return state.has_group("Magic Walls", player)


def fiery_shots(state: CollectionState, player: int) -> bool:
    return state.has_group("Fiery Shots", player)


def heavy_blocks(state: CollectionState, player: int) -> bool:
    return state.has_group("Heavy Blocks", player)


def torches(state: CollectionState, player: int) -> bool:
    return state.has_group("Torches", player)


def dark_rooms(state: CollectionState, player: int) -> bool:
    return state.has_group("Dark Rooms", player)


def grapple(state: CollectionState, player: int) -> bool:
    return state.has_group("Grapple", player)


def levitate(state: CollectionState, player: int) -> bool:
    return state.has_group("Levitate", player)


def secret_vision(state: CollectionState, player: int) -> bool:
    return state.has_group("Secret Vision", player)


def spore_shroud(state: CollectionState, player: int) -> bool:
    return state.has_group("Spore Shroud", player)


def mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Mount", player)


def tar_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Tar Mount", player)


def charging_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Charging Mount", player)
# endregion
