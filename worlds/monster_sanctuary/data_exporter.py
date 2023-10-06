# None of this is used directly by the randomizer
# This file generates a map that's used by the game client to map room names
# to the logical subdivisions that were made for the world.
# Since location names are structured based on room name and object id, the client
# would otherwise have no idea about the logical divisions we make in a single room
import json

from worlds.monster_sanctuary import data_importer, locations, MonsterSanctuaryLocationCategory

if __name__ == '__main__':
    region_map = {}
    monsters = []
    data_importer.load_world()

    for location_name in locations.locations_data:
        data = locations.locations_data[location_name]

        # Start by adding all monsters to the monster list.
        if (data.category == MonsterSanctuaryLocationCategory.MONSTER
                or data.category == MonsterSanctuaryLocationCategory.CHAMPION):
            monsters.append(data.name)

        # The client doesn't care about flags
        if data.category == MonsterSanctuaryLocationCategory.FLAG:
            continue

        parts = data.region.split('_')

        # Because regions normally are structured like
        # "{area name}_{room name}"
        # Any region that has more than 1 underscore has been subdivided
        # Ignore regions that only have 1 underscore
        if len(parts) <= 2:
            continue

        # We reconstruct the location name without the subdivision,
        # which is what the game client will use
        location_name = f"{parts[0]}_{parts[1]}"
        if data.object_id is not None:
            location_name += f"_{data.object_id}"

        if (data.category == MonsterSanctuaryLocationCategory.MONSTER
                or data.category == MonsterSanctuaryLocationCategory.CHAMPION):
            location_name = f"{location_name}_{data.monster_id}"
        elif data.category == MonsterSanctuaryLocationCategory.RANK:
            location_name += "_Champion"

        region_map[location_name] = data.name

    # Serializing and write subsections
    json_object = json.dumps(region_map, indent=4)
    with open("data/subsections.json", "w") as outfile:
        outfile.write(json_object)

    # Serializing and write monster/champion locations
    json_object = json.dumps(monsters, indent=4)
    with open("data/monster_locations.json", "w") as outfile:
        outfile.write(json_object)

