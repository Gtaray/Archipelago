from BaseClasses import MultiWorld, Region, Entrance, Location
from . import rules
from .locations import location_table, MonsterSanctuaryLocation

rooms = {
    "Menu",
    "MountainPath_North1",
    "MountainPath_North2",
    "MountainPath_North3",
    "MountainPath_North4",
    "MountainPath_North5",
    "MountainPath_North6",
    "MountainPath_North7",
    "MountainPath_NorthHidden",
    "MountainPath_East1",
    "MountainPath_Center1",
    "MountainPath_Center2",
    "MountainPath_Center3",
    "MountainPath_Center4",
    "MountainPath_Center5",
    "MountainPath_Center6",
    "MountainPath_Center7",
    "MountainPath_West1",
    "MountainPath_West2",
    "MountainPath_West3",
    "MountainPath_West4",
    "MountainPath_West5",
    "MountainPath_West6",
    "MountainPath_WestHidden",
    "MountainPath_WestHidden2",
    "MountainPath_SnowyEntrance",
    "MountainPath_SnowyEntrance2",
}


class MonsterSanctuaryRegion(Region):
    game: str = "Monster Sanctuary"

    def __init(self, name: str, player: int, world: MultiWorld):
        super(MonsterSanctuaryRegion, self).__init__(name, player, world)


def create_regions(world: MultiWorld, player: int):
    # This should build the regions
    # then connect all the locations to those regions
    region_dict = {room: MonsterSanctuaryRegion(room, player, world) for room in rooms}

    for location in location_table:
        region_dict[location.region].locations += [MonsterSanctuaryLocation(
            player, location.name, location.category, location.default_item, location.id, region_dict[location.region])]

    # add the created regions (which have no extra data in them at this point) to the world.regions set
    # We do this here to that the connect() calls below can properly create Entrances between regions
    world.regions += list(region_dict.values())

    # region Mountain Path
    connect(world, player, "Menu", "MountainPath_North1")
    connect(world, player, "MountainPath_North1", "MountainPath_North2")
    connect(world, player, "MountainPath_North2", "MountainPath_North3")
    connect(world, player, "MountainPath_North3", "MountainPath_North4")
    connect(world, player, "MountainPath_North4", "MountainPath_North5")
    connect(world, player, "MountainPath_North5", "MountainPath_NorthHidden", one_way=True,
            rule=lambda state: rules.has_double_jump(state, player) or
                               rules.improved_flying(state, player) or
                               rules.dual_mobility(state, player) or
                               rules.lofty_mount(state, player))
    connect(world, player, "MountainPath_NorthHidden", "MountainPath_North5", one_way=True)
    connect(world, player, "MountainPath_North5", "MountainPath_East1",
            rule=lambda state: rules.keeper_rank_1(state, player))
    connect(world, player, "MountainPath_North5", "MountainPath_Center1")
    connect(world, player, "MountainPath_Center1", "MountainPath_Center2")
    connect(world, player, "MountainPath_Center2", "MountainPath_Center3")
    connect(world, player, "MountainPath_Center3", "MountainPath_Center4")
    connect(world, player, "MountainPath_Center3", "MountainPath_Center5")
    connect(world, player, "MountainPath_Center3", "MountainPath_Center7",
            rule=lambda state: rules.has_region_key(state, player, "MountainPath"))
    connect(world, player, "MountainPath_Center5", "MountainPath_West1")
    connect(world, player, "MountainPath_West1", "MountainPath_West2")
    connect(world, player, "MountainPath_West2", "MountainPath_West3")
    connect(world, player, "MountainPath_West2", "MountainPath_West4")
    connect(world, player, "MountainPath_West2", "MountainPath_West5")
    connect(world, player, "MountainPath_West2", "MountainPath_SnowyEntrance")
    connect(world, player, "MountainPath_West2", "MountainPath_WestHidden",
            rule=lambda state: rules.breakable_walls(state, player))
    connect(world, player, "MountainPath_West2", "MountainPath_WestHidden2",
            rule=lambda state: rules.narrow_corridors(state, player))
    connect(world, player, "MountainPath_West3", "MountainPath_North6")
    connect(world, player, "MountainPath_North6", "MountainPath_North7", one_way=True,
            rule=lambda state: rules.has_double_jump(state, player) or
                               rules.improved_flying(state, player) or
                               rules.dual_mobility(state, player) or
                               rules.lofty_mount(state, player))
    connect(world, player, "MountainPath_North7", "MountainPath_North6", one_way=True)
    connect(world, player, "MountainPath_North7", "MountainPath_North1", one_way=True)
    connect(world, player, "MountainPath_North1", "MountainPath_North7", one_way=True,
            rule=lambda state: rules.has_double_jump(state, player) or
                               rules.improved_flying(state, player) or
                               rules.dual_mobility(state, player))
    connect(world, player, "MountainPath_West4", "MountainPath_West6")
    connect(world, player, "MountainPath_West5", "MountainPath_Center6")
    connect(world, player, "MountainPath_Center6", "MountainPath_Center7", one_way=True,
            rule=lambda state: rules.has_double_jump(state, player) or
                               rules.improved_flying(state, player) or
                               rules.dual_mobility(state, player))
    connect(world, player, "MountainPath_Center7", "MountainPath_Center6", one_way=True)
    connect(world, player, "MountainPath_SnowyEntrance", "MountainPath_SnowyEntrance2",
            rule=lambda state: rules.has_double_jump(state, player) and (
                    rules.flying(state, player) or
                    rules.improved_flying(state, player) or
                    rules.dual_mobility(state, player)))
    # endregion


def connect(world: MultiWorld,
            player: int,
            source: str,
            target: str,
            rule: callable = lambda state: True,
            one_way=False,
            name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        connect(world, player, target, source, rule, True)
