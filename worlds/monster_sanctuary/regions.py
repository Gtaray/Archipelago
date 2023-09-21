from BaseClasses import MultiWorld, Region, Entrance, Location
from typing import List, Optional, Dict
from . import rules
# from .locations import location_table, MonsterSanctuaryLocation
from .locations import MonsterSanctuaryLocationCategory as LocationCategory, MonsterSanctuaryLocation
from .rules import AccessCondition, Operation


class MonsterSanctuaryConnection:
    def __init__(self, region: str, access_rules: Optional[AccessCondition]):
        self.region = region
        self.access_rules = access_rules


class MonsterSanctuaryRegion(Region):
    game: str = "Monster Sanctuary"
    connections: List[MonsterSanctuaryConnection]

    def __init__(self, name: str, player: int, world: MultiWorld):
        super(MonsterSanctuaryRegion, self).__init__(name, player, world)
        self.connections: List[MonsterSanctuaryConnection] = []

    def add_chest(self, player, chest_data, region_name, location_id):
        chest_name = f"{region_name}_{chest_data['id']}"

        location = MonsterSanctuaryLocation(
            player=player,
            name=chest_name,
            address=location_id,
            category=LocationCategory.CHEST,
            default_item=chest_data["item"],
            access_rule=AccessCondition(chest_data.get("requirements"))
        )

        self.locations += [location]
        return location

    def add_gift(self, player, gift_data, region_name, location_id):
        gift_name = f"{region_name}_{gift_data['id']}"

        location = MonsterSanctuaryLocation(
            player=player,
            name=gift_name,
            address=location_id,
            category=LocationCategory.CHEST,
            default_item=gift_data["item"],
            access_rule=AccessCondition(gift_data.get("requirements"))
        )

        self.locations += [location]
        return location

    def add_encounter(self, player, encounter_data, region_name, location_id, category = LocationCategory.MONSTER):
        result: Dict[int, MonsterSanctuaryLocation] = {}
        encounter_name = f"{region_name}_{encounter_data['id']}"

        i = 0
        for monster in encounter_data["monsters"]:
            location = MonsterSanctuaryLocation(
                player=player,
                name=f"{encounter_name}_{i}",
                address=location_id,
                category=category,
                default_item=monster,
                access_rule=AccessCondition(encounter_data.get("requirements"))
            )

            self.locations += [location]
            result[location_id] = location
            i += 1
            location_id += 1

        return result, location_id

    def add_champion(self, player, champion_data, region_name, location_id):
        event_name = f"{region_name}_Champion"

        rank_event = MonsterSanctuaryLocation(
            player=player,
            name=event_name,
            address=location_id,
            default_item=None,
            category=LocationCategory.RANK,
            access_rule=AccessCondition(champion_data.get("requirements"))
        )
        location_id += 1

        new_locations, location_id = self.add_encounter(
            player,
            champion_data,
            region_name,
            location_id,
            LocationCategory.CHAMPION)

        new_locations[rank_event.address] = rank_event
        return new_locations, location_id

    def add_flag(self, player, flag_data, region_name, location_id):
        location = MonsterSanctuaryLocation(
            player=player,
            name=flag_data["id"],
            address=location_id,
            category=LocationCategory.FLAG,
            access_rule=AccessCondition(flag_data.get("requirements"))
        )
        self.locations += [location]
        return location


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
