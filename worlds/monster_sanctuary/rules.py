from BaseClasses import CollectionState
from typing import List, Optional, Dict
from enum import Enum


class Operation(Enum):
    NONE = 0
    OR = 1
    AND = 2,


class AccessCondition:
    function_name: Optional[str] = None
    invert: bool = False

    def __init__(self, requirements: List[object], operation: Operation = Operation.NONE):
        self.operands: List[AccessCondition] = []
        self.operation: Operation = operation
        self.access_rule = None

        if not requirements:
            self.access_rule = lambda state, player: True
            return

        if len(requirements) == 1:
            params = requirements[0].split()
            if len(params) == 2:
                self.invert = params[0].lower() == "not"
                self.function_name = params[1]
            else:
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
        # We use a while loop here because the for loop will ignore the manually adjustments
        # that are made to i inside the loop, which will result in excessive operands when
        # reqs are nested
        i = 0
        while i < len(requirements):
            op = Operation.NONE

            if requirements[i] == "AND":
                op = Operation.AND
                i += 1
            elif requirements[i] == "OR":
                op = Operation.OR
                i += 1

            reqs = requirements[i]
            if isinstance(reqs, str):
                reqs = [reqs]
            self.operands += [AccessCondition(reqs, op)]

            i += 1

    def __str__(self) -> str:
        if len(self.operands) > 0:
            joiner = " "
            if self.operation == Operation.AND:
                joiner = "&&"
            elif self.operation == Operation.OR:
                joiner = "||"
            return f"({joiner.join([op.__str__() for op in self.operands])})"

        if self.function_name is None:
            return "No Conditions"

        if self.invert:
            return f"NOT {self.function_name}"

        return self.function_name

    def is_leaf(self) -> bool:
        return self.operation is Operation.NONE and len(self.operands) == 0

    def has_access(self, state: CollectionState, player: int) -> bool:
        # if this node has no child conditions, return its own state
        if self.is_leaf():
            if self.access_rule is None:
                return True

            if self.invert:
                return not self.access_rule(state, player)
            else:
                return self.access_rule(state, player)

        # If there are no operands to operate on, then return true
        if not self.operands:
            return True

        # If all operands resolve to true, then return true
        if self.operation == Operation.AND:
            return all([condition.has_access(state, player) for condition in self.operands])
        else:
            return any([condition.has_access(state, player) for condition in self.operands])


class Plotless:
    def __init__(self,
                 type: str,
                 requirements: AccessCondition,
                 connection: Optional[str],
                 object_id: Optional[int],
                 id: Optional[str]):
        self.type = type
        self.access_rules = requirements
        self.connection = connection  # For connections
        self.object_id = object_id  # For locations
        self.id = id  # For flags


plotless_data: Dict[str, List[Plotless]] = {}


def get_plotless_connection(region_name: str, connection: str) -> Optional[Plotless]:
    if region_name not in plotless_data:
        return None

    for entry in plotless_data[region_name]:
        if entry.connection == connection:
            return entry

    return None


def get_plotless_location(region_name: str, object_id: int) -> Optional[Plotless]:
    if region_name not in plotless_data:
        return None

    for entry in plotless_data[region_name]:
        if entry.object_id == object_id:
            return entry

    return None


def get_plotless_flag(region_name: str, flag_id: str) -> Optional[Plotless]:
    if region_name not in plotless_data:
        return None

    for entry in plotless_data[region_name]:
        if entry.id == flag_id:
            return entry

    return None


# region Navigation Flags
def blue_cave_switches_access(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves Switches Access", player)


def blue_cave_champion_room_2_west_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves to Mountain Path Shortcut", player)


def blue_caves_story_complete(state: CollectionState, player: int) -> bool:
    return state.has("Blue Caves Story Complete", player)


def stronghold_dungeon_south_3_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Stronghold Dungeon South 3 Shortcut", player)


def stronghold_dungeon_west_4_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Stronghold Dungeon to Blue Caves Shortcut", player)


def snowy_peaks_east4_upper_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks East 4 Upper Shortcut", player)


def snowy_peaks_east_mountain_3_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks East Mountain 3 Shortcut", player)


def snowy_peaks_sun_palace_entrance_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Snowy Peaks to Sun Palace Shortcut", player)


def has_dodo(state: CollectionState, player: int) -> bool:
    return state.has("Dodo", player) or state.has("Dodo Egg", player)


def stronghold_dungeon_library_access(state: CollectionState, player: int) -> bool:
    return state.has("Stronghold Dungeon Library Access", player)


def sun_palace_raise_center_1(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace Raise Center", player, 1)


def sun_palace_raise_center_2(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace Raise Center", player, 2)


def sun_palace_raise_center_3(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace Raise Center", player, 3)


def sun_palace_lower_water_1(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace Lower Water", player, 1)


def sun_palace_lower_water_2(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace Lower Water", player, 2)


def sun_palace_east_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace East Shortcut", player, 1)


def sun_palace_west_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Sun Palace West Shortcut", player, 1)


def shifting_avialable(state: CollectionState, player: int) -> bool:
    # Either shifting is allowed any time, or we have raised the center 3 times
    return (state.multiworld.worlds[player].options.monster_shift_rule == "any_time" or (
                state.multiworld.worlds[player].options.monster_shift_rule == "after_sun_palace" and
                state.has("Sun Palace Raise Center", player, 3)
            ))


def ancient_woods_east_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Ancient Woods East Shortcut", player, 1)


def ancient_woods_beach_access(state: CollectionState, player: int) -> bool:
    return state.has("Ancient Woods Beach Access", player, 1)


def ancient_woods_magma_chamber_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Ancient Woods to Magma Chamber Shortcut", player, 2)


def goblin_king_defeated(state: CollectionState, player: int) -> bool:
    return state.has("Goblin King Defeated", player)


def horizon_beach_center_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Horizon Beach Center Shortcut", player)


def horizon_beach_rescue_leonard(state: CollectionState, player: int) -> bool:
    return state.has("Rescued Leonard", player)


def horizon_beach_to_magma_chamber_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Horizon Beach To Magma Chamber Shortcut", player)


def magma_chamber_north_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber North Shortcut", player)


def magma_chamber_center_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber Center Shortcut", player)


def magma_chamber_east_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber East Shortcut", player)


def magma_chamber_south_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber South Shortcut", player)


def magma_chamber_lower_lava(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber Lowered Lava", player)


def first_bex_encounter(state: CollectionState, player: int) -> bool:
    return state.has("Bex", player)


def second_bex_encounter(state: CollectionState, player: int) -> bool:
    return state.has("Bex", player, 2)


def third_bex_encounter(state: CollectionState, player: int) -> bool:
    return state.has("Bex", player, 3)


def fourth_bex_encounter(state: CollectionState, player: int) -> bool:
    return state.has("Bex", player, 4)


def forgotten_world_to_horizon_beach_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World to Horizon Beach Shortcut", player)


def forgotten_world_to_magma_chamber_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World to Magma Chamber Shortcut", player)


def underworld_east_catacomb_7_access(state: CollectionState, player: int) -> bool:
    return state.has("Underworld East Catacomb 7 Access", player)


def underworld_east_catacomb_8_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Underworld East Catacomb 8 Shortcut", player)


def underworld_east_catacomb_6_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Underworld East Catacomb 6 Shortcut", player)


def underworld_east_catacomb_pillar_control(state: CollectionState, player: int) -> bool:
    return state.has("Underworld East Catacomb Pillar Control", player)


def underworld_west_catacomb_center_entrance(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb Center Entrance", player)


def underworld_west_catacomb_4_access(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb 4 Access", player)


def underworld_west_catacomb_4_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb 4 Shortcut", player)


def underworld_west_catacomb_7_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb 7 Shortcut", player)


def underworld_west_catacomb_9_interior_access(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb 9 Interior Access", player)


def underworld_west_catacomb_roof_access(state: CollectionState, player: int) -> bool:
    return state.has("Underworld West Catacomb Roof Access", player)


def underworld_to_sun_palace_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Underworld to Sun Palace Shortcut", player)


def mystical_workshop_north_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Mystical Workshop North Shortcut", player)


def abandoned_tower_access(state: CollectionState, player: int) -> bool:
    return state.has("Abandoned Tower Access", player)


def blob_key_accessible(state: CollectionState, player: int) -> bool:
    return state.has("Blob Key Accessible", player)


def all_blob_keys_used(state: CollectionState, player: int) -> bool:
    return state.has("Blob Key Used", player, 3)


def blob_burg_access_1(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 1)


def blob_burg_access_2(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 2)


def blob_burg_access_3(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 3)


def blob_burg_access_4(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 4)


def blob_burg_access_5(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 5)


def blob_burg_access_6(state: CollectionState, player: int) -> bool:
    return state.has("Blob Burg Access", player, 6)


def forgotten_world_jungle_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World Jungle Shortcut", player)


def forgotten_world_caves_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World Caves Shortcut", player)


def forgotten_world_waters_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World Waters Shortcut", player)


def forgotten_world_dracomer_defeated(state: CollectionState, player: int) -> bool:
    return state.has("Forgotten World Dracomer Defeated", player)


def abandoned_tower_south_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Abandoned Tower South Shortcut", player)


def abandoned_tower_center_shortcut(state: CollectionState, player: int) -> bool:
    return state.has("Abandoned Tower Center Shortcut", player)


def post_game(state: CollectionState, player: int) -> bool:
    return state.has("Mad Lord Defeated", player)
# endregion


# region game options
def no_locked_doors(state: CollectionState, player: int) -> bool:
    return state.multiworld.worlds[player].options.remove_locked_doors == 2


def minimal_locked_doors(state: CollectionState, player: int) -> bool:
    return state.multiworld.worlds[player].options.remove_locked_doors == 1
# endregion


# region Keeper battles
def ostanes(state: CollectionState, player: int) -> bool:
    return state.has("Ostanes", player, 1)
# endregion


# region Key Items
def double_jump(state: CollectionState, player: int) -> bool:
    return state.has("Double Jump Boots", player, 1)


def warm_underwear(state: CollectionState, player: int) -> bool:
    return state.has("Warm Underwear", player, 1)


def raw_hide(state: CollectionState, player: int) -> bool:
    return state.has("Raw Hide", player)


def all_sanctuary_tokens(state: CollectionState, player: int) -> bool:
    return state.has("Sanctuary Token", player, 5)


def memorial_ring(state: CollectionState, player: int) -> bool:
    return state.has("Memorial Ring", player, 1)


def all_rare_seashells(state: CollectionState, player: int) -> bool:
    return state.has("Rare Seashell", player, 5)


def runestone_shard(state: CollectionState, player: int) -> bool:
    return state.has("Runestone Shard", player)


def mozzie(state: CollectionState, player: int) -> bool:
    return state.has("Mozzie", player)


def blob_key(state: CollectionState, player: int) -> bool:
    return state.has("Blob Key", player)


def key_of_power(state: CollectionState, player: int) -> bool:
    return state.has("Key of Power", player)


def all_celestial_feathers(state: CollectionState, player: int) -> bool:
    return state.has("Celestial Feather", player, 3)
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
    return state.has("Champion Defeated", player, 27)
# endregion


# region Area Keys.
def mountain_path_key(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Mountain Path key", player, count)


def one_blue_cave_key(state: CollectionState, player: int) -> bool:
    return state.has("Blue Cave key", player)


def two_blue_cave_keys(state: CollectionState, player: int) -> bool:
    return state.count("Blue Cave key", player) >= 2


def three_blue_cave_keys(state: CollectionState, player: int) -> bool:
    return state.count("Blue Cave key", player) >= 3


def one_dungeon_key(state: CollectionState, player: int) -> bool:
    return state.has("Stronghold Dungeon key", player)


def two_dungeon_keys(state: CollectionState, player: int) -> bool:
    return state.count("Stronghold Dungeon key", player) >= 2


def two_ancient_woods_keys(state: CollectionState, player: int) -> bool:
    return state.count("Ancient Woods key", player) >= 2


def three_ancient_woods_keys(state: CollectionState, player: int) -> bool:
    return state.count("Ancient Woods key", player) >= 3


def one_magma_chamber_key(state: CollectionState, player: int) -> bool:
    return state.has("Magma Chamber key", player)


def two_magma_chamber_keys(state: CollectionState, player: int) -> bool:
    return state.count("Magma Chamber key", player) >= 2


def three_workshop_keys(state: CollectionState, player: int) -> bool:
    return state.count("Mystical Workshop key", player) >= 3


def underworld_key(state: CollectionState, player: int) -> bool:
    return state.has("Underworld key", player)


def ahrimaaya(state: CollectionState, player: int, count: int = 1) -> bool:
    return state.has("Ahrimaaya", player, count)
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


def mount(state: CollectionState, player: int) -> bool:
    return (basic_mount(state, player)
            or sonar_mount(state, player)
            or tar_mount(state, player)
            or charging_mount(state, player)
            or lofty_mount(state, player))


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
    return (state.has_group("Ice Orbs", player)
            or check_evolution("Minitaur", "Shard of Winter", state, player))


def distant_ice_orbs(state: CollectionState, player: int) -> bool:
    return state.has_group("Distant Ice Orbs", player)


def summon_rock(state: CollectionState, player: int) -> bool:
    return state.has_group("Summon Rock", player)


def summon_mushroom(state: CollectionState, player: int) -> bool:
    return state.has_group("Summon Mushroom", player)


def summon_big_rock(state: CollectionState, player: int) -> bool:
    return (state.has_group("Summon Big Rock", player)
            or check_evolution("Rocky", "Giant Seed", state, player))


def flying(state: CollectionState, player: int) -> bool:
    return state.has_group("Flying", player)


def improved_flying(state: CollectionState, player: int) -> bool:
    return (state.has_group("Improved Flying", player)
            or check_evolution("Draconov", "Fire Stone", state, player)
            or check_evolution("Draconov", "Ice Stone", state, player)
            or check_evolution("Draconov", "Dark Stone", state, player)
            or check_evolution("Vaero", "Silver Feather", state, player))


def lofty_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Lofty Mount", player)


def basic_swimming(state: CollectionState, player: int) -> bool:
    return state.has_group("Swimming", player)


def improved_swimming(state: CollectionState, player: int) -> bool:
    return (state.has_group("Improved Swimming", player)
            or check_evolution("Draconov", "Deep Stone", state, player))


def dual_mobility(state: CollectionState, player: int) -> bool:
    return state.has_group("Dual Mobility", player)


def narrow_corridors(state: CollectionState, player: int) -> bool:
    return (state.has_group("Narrow Corridors", player)
            or check_evolution("Blob", "Majestic Crown", state, player)
            or check_evolution("Ice Blob", "Majestic Crown", state, player)
            or check_evolution("Lava Blob", "Majestic Crown", state, player)
            or check_evolution("Rainbow Blob", "Majestic Crown", state, player)
            or check_evolution("Tar Blob", "Majestic Crown", state, player))


def magic_walls(state: CollectionState, player: int) -> bool:
    return state.has_group("Magic Walls", player)


def magic_vines(state: CollectionState, player: int) -> bool:
    return (state.has_group("Magic Vines", player)
            or check_evolution("Fungi", "Druid Soul", state, player))


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
    return (state.has_group("Secret Vision", player)
            or check_evolution("Mad Eye", "Demonic Pact", state, player)
            or check_evolution("Monk", "Primordial Branch", state, player))


def spore_shroud(state: CollectionState, player: int) -> bool:
    return (state.has_group("Spore Shroud", player)
            or check_evolution("Fungi", "Druid Soul", state, player))


def basic_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Mount", player)


def sonar_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Sonar Mount", player)


def tar_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Tar Mount", player)


def charging_mount(state: CollectionState, player: int) -> bool:
    return state.has_group("Charging Mount", player)
# endregion


def check_evolution(base_form: str, evo_item: str, state: CollectionState, player: int) -> bool:
    return (state.has("Tree of Evolution Access", player)
            and state.has(base_form, player) and state.has(evo_item, player))
