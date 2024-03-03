from BaseClasses import CollectionState
from typing import List, Optional, Dict, Callable
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


def shifting_available(state: CollectionState, player: int) -> bool:
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


def four_sanctuary_tokens(state: CollectionState, player: int) -> bool:
    return state.has("Sanctuary Token", player, 4)


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


# region Exploration Obstacles
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
    return (claws(state, player)
            or tackle(state, player)
            or slash(state, player)
            or heavy_punch(state, player)
            or toxic_slam(state, player)
            or light_crush(state, player)
            or crush(state, player)
            or corrosive_jabs(state, player)
            or charging_mount(state, player))


def impassible_vines(state: CollectionState, player: int) -> bool:
    return (claws(state, player)
            or ignite(state, player)
            or slash(state, player)
            or fiery_shots(state, player))


def diamond_blocks(state: CollectionState, player: int) -> bool:
    return light_crush(state, player) or crush(state, player) or charging_mount(state, player)


def fire_orbs(state: CollectionState, player: int) -> bool:
    return ignite(state, player) or fiery_shots(state, player)


def water_orbs(state: CollectionState, player: int) -> bool:
    return bubble_burst(state, player) or corrosive_jabs(state, player)


def lightning_orbs(state: CollectionState, player: int) -> bool:
    return lightning_bolt(state, player) or shock_freeze(state, player)


def earth_orbs(state: CollectionState, player: int) -> bool:
    return (slime_shot(state, player)
            or toxic_slam(state, player)
            or jewel_blast(state, player)
            or toxic_freeze(state, player))


def ice_orbs(state: CollectionState, player: int) -> bool:
    return (freeze(state, player)
            or snowball_toss(state, player)
            or shock_freeze(state, player)
            or toxic_freeze(state, player))


def distant_ice_orbs(state: CollectionState, player: int) -> bool:
    return (snowball_toss(state, player)
            or shock_freeze(state, player)
            or toxic_freeze(state, player))


def narrow_corridors(state: CollectionState, player: int) -> bool:
    return blob_form(state, player) or morph_ball(state, player)


def magic_walls(state: CollectionState, player: int) -> bool:
    return minnesang(state, player)


def magic_vines(state: CollectionState, player: int) -> bool:
    return spore_shroud(state, player)


def heavy_blocks(state: CollectionState, player: int) -> bool:
    return tackle(state, player)


def torches(state: CollectionState, player: int) -> bool:
    return ignite(state, player) or lightning_bolt(state, player) or fiery_shots(state, player)


def dark_rooms(state: CollectionState, player: int) -> bool:
    return (sonar(state, player)
            or light(state, player)
            or sonar_mount(state, player)
            or light_crush(state, player))
# endregion


# region Explore Abilities
def can_use_ability(monster_name: str, state: CollectionState, player: int):
    function_name = monster_name.replace(" ", "_").replace("'", "").lower()
    monster_method = globals()[function_name]
    return monster_method(state, player) and is_explore_ability_available(monster_name, state, player)


def is_explore_ability_available(monster_name: str, state: CollectionState, player: int) -> bool:
    opt = state.multiworld.worlds[player].options.lock_explore_abilities
    if opt == "off":
        return True

    from worlds.monster_sanctuary.encounters import get_monster
    monster = get_monster(monster_name)

    if opt == "type":
        return state.has(monster.explore_type_item, player)
    if opt == "ability":
        return state.has(monster.explore_ability_item, player)
    if opt == "species":
        return state.has(monster.explore_species_item, player)

    return False


def claws(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Spectral Wolf", state, player) or
            can_use_ability("Spectral Lion", state, player) or
            can_use_ability("Molebear", state, player))


def tackle(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Spectral Toad", state, player) or
            can_use_ability("Yowie", state, player) or
            can_use_ability("Steam Golem", state, player) or
            can_use_ability("Vasuki", state, player) or
            can_use_ability("Brawlish", state, player) or
            can_use_ability("Targoat", state, player))


def slash(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Catzerker", state, player) or
            can_use_ability("Minitaur", state, player) or
            can_use_ability("Blade Widow", state, player) or
            can_use_ability("Ucan", state, player))


def heavy_punch(state: CollectionState, player: int) -> bool:
    return can_use_ability("Monk", state, player)


def toxic_slam(state: CollectionState, player: int) -> bool:
    return can_use_ability("Goblin Brute", state, player)


def light_crush(state: CollectionState, player: int) -> bool:
    return can_use_ability("Goblin Miner", state, player)


def crush(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Salahammer", state, player) or
            can_use_ability("Asura", state, player) or
            can_use_ability("Goblin Pilot", state, player) or
            can_use_ability("Darnation", state, player))


def corrosive_jabs(state: CollectionState, player: int) -> bool:
    return can_use_ability("Troll", state, player)


def charging_mount(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Rampede", state, player) or
            can_use_ability("Rathops", state, player))


def ignite(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Magmapillar", state, player) or
            can_use_ability("Tengu", state, player) or
            can_use_ability("Specter", state, player) or
            can_use_ability("Magmamoth", state, player) or
            can_use_ability("Imori", state, player) or
            can_use_ability("Lava Blob", state, player) or
            can_use_ability("Skorch", state, player) or
            can_use_ability("Plague Egg", state, player))


def fiery_shots(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Goblin Hood", state, player) or
            can_use_ability("Polterofen", state, player) or
            can_use_ability("Mimic", state, player))


def bubble_burst(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Blob", state, player) or
            can_use_ability("Grummy", state, player) or
            can_use_ability("G'rulu", state, player))


def lightning_bolt(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Crackle Knight", state, player) or
            can_use_ability("Beetloid", state, player) or
            can_use_ability("Goblin Warlock", state, player) or
            can_use_ability("Sizzle Knight", state, player))


def shock_freeze(state: CollectionState, player: int) -> bool:
    return can_use_ability("Shockhopper", state, player)


def slime_shot(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Toxiquus", state, player) or
            can_use_ability("Ninki", state, player) or
            can_use_ability("Ninki Nanka", state, player))


def jewel_blast(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Goblin King", state, player) or
            can_use_ability("Crystal Snail", state, player))


def toxic_freeze(state: CollectionState, player: int) -> bool:
    return can_use_ability("Spinner", state, player)


def freeze(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Ice Blob", state, player) or
            can_use_ability("Megataur", state, player))


def snowball_toss(state: CollectionState, player: int) -> bool:
    return can_use_ability("Mogwai", state, player)


def flying(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Spectral Eagle", state, player) or
            can_use_ability("Vaero", state, player) or
            can_use_ability("Frosty", state, player) or
            can_use_ability("Mad Eye", state, player) or
            can_use_ability("Raduga", state, player) or
            can_use_ability("Draconov", state, player))


def improved_flying(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Silvaero", state, player) or
            can_use_ability("Kongamato", state, player) or
            can_use_ability("Dracogran", state, player) or
            can_use_ability("Dracozul", state, player) or
            can_use_ability("Draconoir", state, player) or
            can_use_ability("Ornithopter", state, player))


def lofty_mount(state: CollectionState, player: int) -> bool:
    return can_use_ability("Gryphonix", state, player)


def basic_swimming(state: CollectionState, player: int) -> bool:
    return can_use_ability("Koi", state, player)


def improved_swimming(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Thornish", state, player) or
            can_use_ability("Nautilid", state, player) or
            can_use_ability("Elderjel", state, player) or
            can_use_ability("Dracomer", state, player))


def dual_mobility(state: CollectionState, player: int) -> bool:
    return can_use_ability("Krakaturtle", state, player)


def basic_mount(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Aurumtail", state, player) or
            can_use_ability("Qilin", state, player) or
            can_use_ability("Dodo", state, player) or
            can_use_ability("Moccus", state, player))


def sonar_mount(state: CollectionState, player: int) -> bool:
    return can_use_ability("Akhlut", state, player)


def tar_mount(state: CollectionState, player: int) -> bool:
    return can_use_ability("Tar Blob", state, player)


def summon_rock(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Rocky", state, player) or
            can_use_ability("Druid Oak", state, player) or
            can_use_ability("Kame", state, player))


def summon_mushroom(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Fungi", state, player) or
            can_use_ability("Tanuki", state, player))


def summon_big_rock(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Brutus", state, player) or
            can_use_ability("Mega Rock", state, player) or
            can_use_ability("Promethean", state, player))


def sonar(state: CollectionState, player: int) -> bool:
    return can_use_ability("Nightwing", state, player)


def light(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Glowfly", state, player) or
            can_use_ability("Caraglow", state, player) or
            can_use_ability("Manticorb", state, player) or
            can_use_ability("Glowdra", state, player))


def ghost_form(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Sycophantom", state, player) or
            can_use_ability("Kanko", state, player) or
            can_use_ability("Stolby", state, player))


def spore_shroud(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Fumagus", state, player) or
            can_use_ability("Amberlgna", state, player))


def grapple(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Oculus", state, player) or
            can_use_ability("Argiope", state, player) or
            can_use_ability("Arachlich", state, player) or
            can_use_ability("Worm", state, player))


def blob_form(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Rainbow Blob", state, player) or
            can_use_ability("King Blob", state, player))


def morph_ball(state: CollectionState, player: int) -> bool:
    return can_use_ability("Changeling", state, player)


def levitate(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Vodinoy", state, player) or
            can_use_ability("Diavola", state, player) or
            can_use_ability("Vertraag", state, player) or
            can_use_ability("Terradrile", state, player))


def secret_vision(state: CollectionState, player: int) -> bool:
    return (can_use_ability("Sutsune", state, player) or
            can_use_ability("Thanatos", state, player) or
            can_use_ability("Aazerach", state, player) or
            can_use_ability("Mad Lord", state, player) or
            can_use_ability("Ascendant", state, player))


def minnesang(state: CollectionState, player: int) -> bool:
    return can_use_ability("Bard", state, player)
# endregion


# region Monsters
def has_any_monster(state: CollectionState, player: int, *creatures: Callable) -> bool:
    for creature in creatures:
        if creature(state, player):
            return True

    return False


def spectral_wolf(state: CollectionState, player: int) -> bool:
    return has_monster("Spectral Wolf", state, player)


def spectral_toad(state: CollectionState, player: int) -> bool:
    return has_monster("Spectral Toad", state, player)


def spectral_eagle(state: CollectionState, player: int) -> bool:
    return has_monster("Spectral Eagle", state, player)


def spectral_lion(state: CollectionState, player: int) -> bool:
    return has_monster("Spectral Lion", state, player)


def blob(state: CollectionState, player: int) -> bool:
    return has_monster("Blob", state, player)


def magmapillar(state: CollectionState, player: int) -> bool:
    return (has_monster("Magmapillar", state, player)
            or state.has("Magmamoth", player))


def rocky(state: CollectionState, player: int) -> bool:
    return (has_monster("Rocky", state, player)
            or state.has("Mega Rock", player))


def vaero(state: CollectionState, player: int) -> bool:
    return (has_monster("Vaero", state, player)
            or state.has("Silvaero", player))


def catzerker(state: CollectionState, player: int) -> bool:
    return has_monster("Catzerker", state, player)


def yowie(state: CollectionState, player: int) -> bool:
    return has_monster("Yowie", state, player)


def steam_golem(state: CollectionState, player: int) -> bool:
    return has_monster("Steam Golem", state, player)


def monk(state: CollectionState, player: int) -> bool:
    return (has_monster("Monk", state, player)
            or state.has("Ascendant", player))


def grummy(state: CollectionState, player: int) -> bool:
    return (has_monster("Grummy", state, player)
            or state.has("G'rulu", player))


def tengu(state: CollectionState, player: int) -> bool:
    return has_monster("Tengu", state, player)


def fungi(state: CollectionState, player: int) -> bool:
    return (has_monster("Fungi", state, player)
            or state.has("Fumagus", player))


def frosty(state: CollectionState, player: int) -> bool:
    return has_monster("Frosty", state, player)


def minitaur(state: CollectionState, player: int) -> bool:
    return (has_monster("Minitaur", state, player)
             or state.has("Megataur", player))


def specter(state: CollectionState, player: int) -> bool:
    return has_monster("Specter", state, player)


def crackle_knight(state: CollectionState, player: int) -> bool:
    return (has_monster("Crackle Knight", state, player)
            or state.has("Sizzle Knight", player))


def grulu(state: CollectionState, player: int) -> bool:
    return (has_monster("G'rulu", state, player)
            or check_evolution("Grummy", "G'rulu", state, player))


def mad_eye(state: CollectionState, player: int) -> bool:
    return (has_monster("Mad Eye", state, player)
            or state.has("Mad Lord", player))


def nightwing(state: CollectionState, player: int) -> bool:
    return has_monster("Nightwing", state, player)


def toxiquus(state: CollectionState, player: int) -> bool:
    return has_monster("Toxiquus", state, player)


def beetloid(state: CollectionState, player: int) -> bool:
    return has_monster("Beetloid", state, player)


def druid_oak(state: CollectionState, player: int) -> bool:
    return has_monster("Druid Oak", state, player)


def magmamoth(state: CollectionState, player: int) -> bool:
    return (has_monster("Magmamoth", state, player)
            or check_evolution("Magmapillar", "Magmamoth", state, player))


def molebear(state: CollectionState, player: int) -> bool:
    return has_monster("Molebear", state, player)


def glowfly(state: CollectionState, player: int) -> bool:
    return (has_monster("Glowfly", state, player)
            or state.has("Glowdra", player))


def goblin_brute(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin Brute", state, player)


def goblin_hood(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin Hood", state, player)


def goblin_warlock(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin Warlock", state, player)


def goblin_king(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin King", state, player)


def raduga(state: CollectionState, player: int) -> bool:
    return has_monster("Raduga", state, player)


def ice_blob(state: CollectionState, player: int) -> bool:
    return has_monster("Ice Blob", state, player)


def caraglow(state: CollectionState, player: int) -> bool:
    return has_monster("Caraglow", state, player)


def aurumtail(state: CollectionState, player: int) -> bool:
    return has_monster("Aurumtail", state, player)


def megataur(state: CollectionState, player: int) -> bool:
    return (has_monster("Megataur", state, player)
            or check_evolution("Minitaur", "Megataur", state, player))


def mogwai(state: CollectionState, player: int) -> bool:
    return has_monster("Mogwai", state, player)


def crystal_snail(state: CollectionState, player: int) -> bool:
    return has_monster("Crystal Snail", state, player)


def akhlut(state: CollectionState, player: int) -> bool:
    return has_monster("Akhlut", state, player)


def blade_widow(state: CollectionState, player: int) -> bool:
    return has_monster("Blade Widow", state, player)


def ninki(state: CollectionState, player: int) -> bool:
    return (has_monster("Ninki", state, player)
            or state.has("Ninki Nanka", player))


def ninki_nanka(state: CollectionState, player: int) -> bool:
    return (has_monster("Ninki Nanka", state, player)
            or check_evolution("Ninki", "Ninki Nanka", state, player))


def vasuki(state: CollectionState, player: int) -> bool:
    return has_monster("Vasuki", state, player)


def kame(state: CollectionState, player: int) -> bool:
    return has_monster("Kame", state, player)


def sycophantom(state: CollectionState, player: int) -> bool:
    return has_monster("Sycophantom", state, player)


def imori(state: CollectionState, player: int) -> bool:
    return has_monster("Imori", state, player)


def qilin(state: CollectionState, player: int) -> bool:
    return has_monster("Qilin", state, player)


def sizzle_knight(state: CollectionState, player: int) -> bool:
    return (has_monster("Sizzle Knight", state, player)
            or check_evolution("Crackle Knight", "Sizzle Knight", state, player))


def koi(state: CollectionState, player: int) -> bool:
    return has_monster("Koi", state, player)


def tanuki(state: CollectionState, player: int) -> bool:
    return has_monster("Tanuki", state, player)


def kanko(state: CollectionState, player: int) -> bool:
    return has_monster("Kanko", state, player)


def dodo(state: CollectionState, player: int) -> bool:
    return has_monster("Dodo", state, player)


def kongamato(state: CollectionState, player: int) -> bool:
    return has_monster("Kongamato", state, player)


def ucan(state: CollectionState, player: int) -> bool:
    return has_monster("Ucan", state, player)


def brawlish(state: CollectionState, player: int) -> bool:
    return has_monster("Brawlish", state, player)


def thornish(state: CollectionState, player: int) -> bool:
    return has_monster("Thornish", state, player)


def nautilid(state: CollectionState, player: int) -> bool:
    return has_monster("Nautilid", state, player)


def silvaero(state: CollectionState, player: int) -> bool:
    return (has_monster("Silvaero", state, player)
            or check_evolution("Vaero", "Silvaero", state, player))


def elderjel(state: CollectionState, player: int) -> bool:
    return has_monster("Elderjel", state, player)


def manticorb(state: CollectionState, player: int) -> bool:
    return has_monster("Manticorb", state, player)


def goblin_miner(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin Miner", state, player)


def salahammer(state: CollectionState, player: int) -> bool:
    return has_monster("Salahammer", state, player)


def lava_blob(state: CollectionState, player: int) -> bool:
    return has_monster("Lava Blob", state, player)


def glowdra(state: CollectionState, player: int) -> bool:
    return (has_monster("Glowdra", state, player)
            or check_evolution("Glowfly", "Glowdra", state, player))


def draconov(state: CollectionState, player: int) -> bool:
    return (has_monster("Draconov", state, player)
            or state.has("Dracogran", player)
            or state.has("Dracozul", player)
            or state.has("Draconoir", player)
            or state.has("Dracomer", player))


def dracogran(state: CollectionState, player: int) -> bool:
    return (has_monster("Dracogran", state, player)
            or check_evolution("Draconov", "Dracogran", state, player))


def asura(state: CollectionState, player: int) -> bool:
    return has_monster("Asura", state, player)


def skorch(state: CollectionState, player: int) -> bool:
    return has_monster("Skorch", state, player)


def stolby(state: CollectionState, player: int) -> bool:
    return has_monster("Stolby", state, player)


def ornithopter(state: CollectionState, player: int) -> bool:
    return has_monster("Ornithopter", state, player)


def polterofen(state: CollectionState, player: int) -> bool:
    return has_monster("Polterofen", state, player)


def oculus(state: CollectionState, player: int) -> bool:
    return has_monster("Oculus", state, player)


def mimic(state: CollectionState, player: int) -> bool:
    return has_monster("Mimic", state, player)


def goblin_pilot(state: CollectionState, player: int) -> bool:
    return has_monster("Goblin Pilot", state, player)


def shockhopper(state: CollectionState, player: int) -> bool:
    return has_monster("Shockhopper", state, player)


def targoat(state: CollectionState, player: int) -> bool:
    return has_monster("Targoat", state, player)


def dracozul(state: CollectionState, player: int) -> bool:
    return (has_monster("Dracozul", state, player)
            or check_evolution("Draconov", "Dracozul", state, player))


def troll(state: CollectionState, player: int) -> bool:
    return has_monster("Troll", state, player)


def brutus(state: CollectionState, player: int) -> bool:
    return has_monster("Brutus", state, player)


def mega_rock(state: CollectionState, player: int) -> bool:
    return (has_monster("Mega Rock", state, player)
            or check_evolution("Rocky", "Mega Rock", state, player))


def argiope(state: CollectionState, player: int) -> bool:
    return has_monster("Argiope", state, player)


def arachlich(state: CollectionState, player: int) -> bool:
    return has_monster("Arachlich", state, player)


def moccus(state: CollectionState, player: int) -> bool:
    return has_monster("Moccus", state, player)


def promethean(state: CollectionState, player: int) -> bool:
    return has_monster("Promethean", state, player)


def draconoir(state: CollectionState, player: int) -> bool:
    return (has_monster("Draconoir", state, player)
            or check_evolution("Draconov", "Draconoir", state, player))


def spinner(state: CollectionState, player: int) -> bool:
    return has_monster("Spinner", state, player)


def plague_egg(state: CollectionState, player: int) -> bool:
    return has_monster("Plague Egg", state, player)


def sutsune(state: CollectionState, player: int) -> bool:
    return has_monster("Sutsune", state, player)


def darnation(state: CollectionState, player: int) -> bool:
    return has_monster("Darnation", state, player)


def thanatos(state: CollectionState, player: int) -> bool:
    return has_monster("Thanatos", state, player)


def rainbow_blob(state: CollectionState, player: int) -> bool:
    return has_monster("Rainbow Blob", state, player)


def changeling(state: CollectionState, player: int) -> bool:
    return has_monster("Changeling", state, player)


def king_blob(state: CollectionState, player: int) -> bool:
    return (has_monster("King Blob", state, player)
            or check_evolution("Blob", "King Blob", state, player)
            or check_evolution("Ice Blob", "King Blob", state, player)
            or check_evolution("Lava Blob", "King Blob", state, player)
            or check_evolution("Rainbow Blob", "King Blob", state, player)
            or check_evolution("Tar Blob", "King Blob", state, player))


def worm(state: CollectionState, player: int) -> bool:
    return has_monster("Worm", state, player)


def vodinoy(state: CollectionState, player: int) -> bool:
    return has_monster("Vodinoy", state, player)


def aazerach(state: CollectionState, player: int) -> bool:
    return has_monster("Aazerach", state, player)


def diavola(state: CollectionState, player: int) -> bool:
    return has_monster("Diavola", state, player)


def gryphonix(state: CollectionState, player: int) -> bool:
    return has_monster("Gryphonix", state, player)


def vertraag(state: CollectionState, player: int) -> bool:
    return has_monster("Vertraag", state, player)


def mad_lord(state: CollectionState, player: int) -> bool:
    return (has_monster("Mad Lord", state, player)
            or check_evolution("Mad Eye", "Mad Lord", state, player))


def ascendant(state: CollectionState, player: int) -> bool:
    return (has_monster("Ascendant", state, player)
            or check_evolution("Monk", "Ascendant", state, player))


def fumagus(state: CollectionState, player: int) -> bool:
    return (has_monster("Fumagus", state, player)
            or check_evolution("Fungi", "Fumagus", state, player))


def rampede(state: CollectionState, player: int) -> bool:
    return has_monster("Rampede", state, player)


def rathops(state: CollectionState, player: int) -> bool:
    return has_monster("Rathops", state, player)


def krakaturtle(state: CollectionState, player: int) -> bool:
    return has_monster("Krakaturtle", state, player)


def tar_blob(state: CollectionState, player: int) -> bool:
    return has_monster("Tar Blob", state, player)


def amberlgna(state: CollectionState, player: int) -> bool:
    return has_monster("Amberlgna", state, player)


def dracomer(state: CollectionState, player: int) -> bool:
    return (has_monster("Dracomer", state, player)
            or check_evolution("Draconov", "Dracomer", state, player))


def terradrile(state: CollectionState, player: int) -> bool:
    return has_monster("Terradrile", state, player)


def bard(state: CollectionState, player: int) -> bool:
    return has_monster("Bard", state, player)


def has_monster(monster_name: str, state: CollectionState, player: int):
    # First, if we've got the monster, then we return straight away
    if state.has(monster_name, player):
        return True

    # Next we check if we have the monster's egg
    from worlds.monster_sanctuary.encounters import get_monster
    monster = get_monster(monster_name)
    if state.has(monster.egg_name(True), player):
        return True

    return False


def check_evolution(base_form: str, evo_form: str, state: CollectionState, player: int) -> bool:
    # First we check if the evolution is already available to the player
    if has_monster(evo_form, state, player):
        return True

    from worlds.monster_sanctuary.encounters import get_monster
    return (state.has("Tree of Evolution Access", player)
            # Don't need to check if we have the evovolved form, we already did that above.
            # Only need to check if we have the base form and its evo item
            and (has_monster(base_form, state, player))
            and state.has(get_monster(evo_form).catalyst, player))


def has_all_monsters(state: CollectionState, player: int) -> bool:
    from worlds.monster_sanctuary.encounters import monster_data

    # Go through every monster in the game, and if we don't have it, return false
    # if we get through all monsters it means we have everything, and can return true
    for name, data in monster_data.items():
        method_name = name.replace(" ", "_").replace("'", "").lower()

        # check if we have the monster
        if not globals()[method_name](state, player):
            return False

    return True
# endregion
