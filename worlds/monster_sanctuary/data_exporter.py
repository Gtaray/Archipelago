# None of this is used directly by the randomizer
# This file generates a map that's used by the game client to map room names
# to the logical subdivisions that were made for the world.
# Since location names are structured based on room name and object id, the client
# would otherwise have no idea about the logical divisions we make in a single room
import json

from worlds.monster_sanctuary import data_importer, locations, MonsterSanctuaryLocationCategory

if __name__ == '__main__':
    region_map = {}
    number_of_checks = {}

    for location_name in locations.location_data:
        data = locations.location_data[location_name]
        parts = data.region.split('_')

        if (data.category == MonsterSanctuaryLocationCategory.CHEST
                or data.category == MonsterSanctuaryLocationCategory.GIFT):
            if parts[0] not in number_of_checks.keys():
                number_of_checks[parts[0]] = 0
            number_of_checks[parts[0]] += 1

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

        if data.category == MonsterSanctuaryLocationCategory.RANK:
            location_name += "_Champion"

        region_map[location_name] = data.name

    # Serializing and write subsections
    json_object = json.dumps(region_map, indent=4)
    with open("export/subsections.json", "w") as outfile:
        outfile.write(json_object)

    # Serializing the total number of checks for regions
    json_object = json.dumps(number_of_checks, indent=4)
    with open("export/number_of_checks.json", "w") as outfile:
        outfile.write(json_object)

