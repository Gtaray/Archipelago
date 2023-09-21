import json
from typing import List, Optional, Dict

from BaseClasses import MultiWorld
from worlds.monster_sanctuary.locations import MonsterSanctuaryLocation
from worlds.monster_sanctuary.regions import MonsterSanctuaryRegion, MonsterSanctuaryConnection
from worlds.monster_sanctuary.rules import AccessCondition, Operation


def load_world(world: MultiWorld, player: int):
    regions: Dict[str, MonsterSanctuaryRegion] = {}
    locations: Dict[int, MonsterSanctuaryLocation] = {}
    location_id: int = 970500

    with open('worlds/monster_sanctuary/data/world.json') as file:
        data = json.load(file)
        for region_data in data:
            region = MonsterSanctuaryRegion(region_data["region"], player, world)

            for conn_data in region_data.get("connections"):
                requirements = AccessCondition(conn_data.get("requirements"))
                connection = MonsterSanctuaryConnection(conn_data.get("region"), requirements)
                region.connections += [connection]

            region_name: str = region.name
            for chest_data in region_data.get("chests") or []:
                location = region.add_chest(player, chest_data, region_name, location_id)
                locations[location_id] = location
                location_id += 1

            for gift_data in region_data.get("gifts") or []:
                # Hack because we store comments as strings
                if isinstance(gift_data, str):
                    continue
                location = region.add_gift(player, gift_data, region_name, location_id)
                locations[location_id] = location
                location_id += 1

            for encounter_data in region_data.get("encounters") or []:
                result = region.add_encounter(player, encounter_data, region_name, location_id)
                locations.update(result[0])
                location_id = result[1]

            for champion_data in region_data.get("champions") or []:
                result = region.add_encounter(player, champion_data, region_name, location_id)
                locations.update(result[0])
                location_id = result[1]

            for flag_data in region_data.get("flags") or []:
                location = region.add_flag(player, flag_data, region_name, location_id)
                locations[location_id] = location
                location_id += 1

            regions[region.name] = region
