import json
import os
from typing import Optional, Dict

from . import data
from . import regions as REGIONS
from . import items as ITEMS
from . import locations as LOCATIONS
from . import rules as RULES
from . import flags as FLAGS
from . import encounters as ENCOUNTERS
from . import hints as HINTS

from .regions import RegionData, MonsterSanctuaryConnection
from .items import ItemData, MonsterSanctuaryItemCategory
from .locations import LocationData, MonsterSanctuaryLocationCategory
from .rules import AccessCondition
from .flags import FlagData
from .encounters import EncounterData, MonsterData
from BaseClasses import ItemClassification

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa


def load_world() -> None:
    # Clear out old data
    LOCATIONS.location_data.clear()
    ENCOUNTERS.encounter_data.clear()
    FLAGS.flag_data.clear()

    location_names: Dict[str, str] = {}
    locations_by_id: Dict[int, LocationData] = {}
    location_id: int = 970500

    with files(data).joinpath("location_names.json").open() as file:
        location_names = json.load(file)

    with files(data).joinpath("world.json").open() as file:
        json_data = json.load(file)
        for region_data in json_data:
            region = RegionData(region_data["region"])

            if region_data.get("connections") is None:
                raise SyntaxError(f"Region '{region.name}' has no defined connections")

            for conn_data in region_data.get("connections"):
                requirements = AccessCondition(conn_data.get("requirements"))
                connection = MonsterSanctuaryConnection(conn_data.get("region"), requirements)
                region.connections += [connection]

            region_name: str = region.name

            for chest_data in region_data.get("chests") or []:
                # Hack because we store comments as strings
                if isinstance(chest_data, str):
                    continue
                display_name = location_names[f"{region_name}_{chest_data['id']}"]
                location = add_chest_location(location_id, display_name, chest_data, region_name)
                locations_by_id[location_id] = location
                location_id += 1

            for gift_data in region_data.get("gifts") or []:
                # Hack because we store comments as strings
                if isinstance(gift_data, str):
                    continue
                display_name = location_names[f"{region_name}_{gift_data['id']}"]
                location = add_gift_location(location_id, display_name, gift_data, region_name)
                locations_by_id[location_id] = location
                location_id += 1

            for eggsanity_data in region_data.get("eggsanity") or []:
                # Hack because we store comments as strings
                if isinstance(eggsanity_data, str):
                    continue
                logical_name = f"eggsanity_{eggsanity_data['id']}"
                display_name = location_names[logical_name]
                location = add_eggsanity_location(location_id, logical_name, display_name, region_name, eggsanity_data)
                locations_by_id[location_id] = location
                location_id += 1

            for army_data in region_data.get("army") or []:
                # Hack because we store comments as strings
                if isinstance(eggsanity_data, str):
                    continue

                reward_index = 0
                for reward in army_data.get("items"):
                    logical_name = f"KeeperStronghold_MonsterArmy_{army_data['id']}_{reward_index}"
                    display_name = location_names[logical_name]
                    location = add_army_reward_location(location_id, logical_name, display_name, region_name, army_data, reward)
                    locations_by_id[location_id] = location
                    location_id += 1
                    reward_index += 1

            for encounter_data in region_data.get("encounters") or []:
                # Hack because we store comments as strings
                if isinstance(encounter_data, str):
                    continue

                add_encounter_data(encounter_data, region_name)

            for champion_data in region_data.get("champion") or []:
                # Hack because we store comments as strings
                if isinstance(champion_data, str):
                    continue

                # First add the rank up item
                display_name = location_names[f"{region_name}_Champion"]
                location = add_rank_location(location_id, display_name, champion_data, region_name)
                locations_by_id[location_id] = location
                location_id += 1

                add_champion_data(champion_data, region_name)

            for flag_data in region_data.get("flags") or []:
                # Hack because we store comments as strings
                if isinstance(flag_data, str):
                    continue
                add_flag_data(flag_data, region_name)

            for shop_data in region_data.get("shops") or []:
                # Hack because we store comments as strings
                if isinstance(shop_data, str):
                    continue
                location_id = add_shop_locations(shop_data, locations_by_id, location_id, region_name)

            REGIONS.region_data[region.name] = region


def load_items(item_id: int) -> int:

    with files(data).joinpath("items.json").open() as file:
        items_file = json.load(file)
        for item_category_data in items_file:
            item_category = parse_item_type(item_category_data["type"])
            if item_category is None:
                raise KeyError(f"Item Type '{item_category}' does not match any existing item types")

            default_classification = parse_item_classification(item_category_data.get("classification"))

            for item_data in item_category_data["items"]:
                # Prioritize the item's classification, but fall back to the category's
                # classification. If both are empty, throw an error.
                item_classification = parse_item_classification(item_data.get("classification"))
                if item_classification is None:
                    item_classification = default_classification
                if item_classification is None:
                    raise KeyError(f"Item Classification for item '{item_data['name']}' is missing")

                item = ItemData(
                    item_id,
                    item_data["name"],
                    item_classification,
                    item_category,
                    item_data.get("tier"),
                    item_data.get("unique") or False,
                    item_data.get("groups")
                )

                if item_category == MonsterSanctuaryItemCategory.KEYITEM:
                    item.count = item_data.get("count") or 1

                ITEMS.item_data[item.name] = item
                item_id += 1

    # This json file has a list of places where items are not allowed to be placed
    with files(data).joinpath("item_rules.json").open() as file:
        item_rules = json.load(file)
        for item_data in item_rules:
            item_name = item_data["item"]
            locations = item_data["locations"]

            item = ITEMS.get_item_by_name(item_name)
            item.illegal_locations = locations

    return item_id


def load_monsters(item_id) -> int:
    with files(data).joinpath("monsters.json").open() as file:
        monster_file = json.load(file)

        for monster_data in monster_file:
            name = monster_data["Name"]
            groups = monster_data.get("Groups")
            if groups is None:
                raise ValueError(f"{name} has no groups assigned to it")
            if monster_data["SpeciesItem"] not in ITEMS.item_data:
                raise KeyError(f"SpeciesItem '{monster_data['SpeciesItem']}' is not a valid item")
            if monster_data["AbilityItem"] not in ITEMS.item_data:
                raise KeyError(f"AbilityItem '{monster_data['AbilityItem']}' is not a valid item")
            if monster_data["TypeItem"] not in ITEMS.item_data:
                raise KeyError(f"TypeItem '{monster_data['TypeItem']}' is not a valid item")

            monster = MonsterData(
                item_id,
                name,
                groups)

            monster.explore_species_item = monster_data["SpeciesItem"]
            monster.explore_ability_item = monster_data["AbilityItem"]
            monster.explore_type_item = monster_data["TypeItem"]

            ENCOUNTERS.monster_data[name] = monster
            item_id += 1

    return item_id


def load_flags(item_id) -> int:
    with files(data).joinpath("flags.json").open() as file:
        flags_file = json.load(file)

        for flag_item in flags_file:
            name = flag_item["name"]
            classification = parse_item_classification(flag_item["classification"])
            FLAGS.set_flag_item_id(name, item_id, classification)
            item_id += 1

    return item_id


def load_hints():
    with files(data).joinpath("hints.json").open() as file:
        hints_file = json.load(file)

        for hint in hints_file["preset"]:
            HINTS.hint_data[hint["id"]] = HINTS.HintData(hint)


def parse_item_type(text) -> Optional[MonsterSanctuaryItemCategory]:
    if text == "Rank":
        return MonsterSanctuaryItemCategory.RANK
    elif text == "Key Item":
        return MonsterSanctuaryItemCategory.KEYITEM
    elif text == "Crafting Material":
        return MonsterSanctuaryItemCategory.CRAFTINGMATERIAL
    elif text == "Consumable":
        return MonsterSanctuaryItemCategory.CONSUMABLE
    elif text == "Food":
        return MonsterSanctuaryItemCategory.FOOD
    elif text == "Catalyst":
        return MonsterSanctuaryItemCategory.CATALYST
    elif text == "Weapon":
        return MonsterSanctuaryItemCategory.WEAPON
    elif text == "Accessory":
        return MonsterSanctuaryItemCategory.ACCESSORY
    elif text == "Currency":
        return MonsterSanctuaryItemCategory.CURRENCY
    elif text == "Egg":
        return MonsterSanctuaryItemCategory.EGG
    elif text == "Costume":
        return MonsterSanctuaryItemCategory.COSTUME
    elif text == "Explore Ability":
        return MonsterSanctuaryItemCategory.ABILITY
    elif text == "Trap":
        return MonsterSanctuaryItemCategory.TRAP
    elif text == "Combat Trap":
        return MonsterSanctuaryItemCategory.COMBATTRAP

    return None


def parse_item_classification(text: Optional[str]) -> Optional[ItemClassification]:
    if text == "filler":
        return ItemClassification.filler
    elif text == "progression":
        return ItemClassification.progression
    elif text == "useful":
        return ItemClassification.useful
    elif text == "trap":
        return ItemClassification.trap
    elif text == "skip_balancing":
        return ItemClassification.skip_balancing
    elif text == "progression_skip_balancing":
        return ItemClassification.progression_skip_balancing

    return None


# region Data Adders
def add_location(location_id, location_name, json_data, region_name, category: MonsterSanctuaryLocationCategory):
    location = LocationData(
        location_id=location_id,
        name=location_name,
        region=region_name,
        category=category,
        default_item=json_data["item"],
        access_condition=AccessCondition(json_data.get("requirements")),
        object_id=json_data["id"],
        hint=json_data.get("hint")
    )

    LOCATIONS.add_location(f"{region_name}_{json_data['id']}", location)
    return location


def add_chest_location(location_id, location_name, chest_data, region_name) -> LocationData:
    return add_location(location_id, location_name, chest_data, region_name, MonsterSanctuaryLocationCategory.CHEST)


def add_gift_location(location_id, location_name, gift_data, region_name) -> LocationData:
    return add_location(location_id, location_name, gift_data, region_name, MonsterSanctuaryLocationCategory.GIFT)


def add_eggsanity_location(location_id, logical_name, location_name, region_name, json_data):
    location = LocationData(
        location_id=location_id,
        name=location_name,
        region=region_name,
        category=MonsterSanctuaryLocationCategory.EGGSANITY,
        access_condition=AccessCondition(json_data.get("requirements")),
    )

    LOCATIONS.add_location(logical_name, location)
    return location


def add_shop_locations(shop_data, locations_by_id, location_id, region_name):
    shop_name = shop_data["name"]
    inventory = shop_data["inventory"]

    for item in inventory:
        # Hack 'cause comments are strings
        if isinstance(item, str):
            continue

        item_name = item["item"]
        inventory_id = item["id"]
        logical_name = f"{region_name}_{shop_name.replace(' ', '')}_{inventory_id}"
        location = LocationData(
            location_id=location_id,
            name=f"{shop_name} - {item_name}",
            region=region_name,
            category=MonsterSanctuaryLocationCategory.SHOP,
            default_item=item_name,
            access_condition=AccessCondition(item.get("requirements"))
        )
        location.logical_name = logical_name

        if item.get("limited") is not None:
            location.shop_is_limited = item["limited"]

        LOCATIONS.add_location(logical_name, location)
        location_id += 1

    return location_id


def add_army_reward_location(location_id, logical_name, display_name, region_name, army_data, reward):
    location = LocationData(
        location_id=location_id,
        name=display_name,
        region=region_name,
        category=MonsterSanctuaryLocationCategory.ARMY,
        default_item=reward,
        access_condition=AccessCondition(army_data.get("requirements"))
    )

    LOCATIONS.add_location(logical_name, location)
    return location


def add_rank_location(location_id, display_name, champion_data, region_name) -> LocationData:
    rank_location = LocationData(
        location_id=location_id,
        name=display_name,
        region=region_name,
        category=MonsterSanctuaryLocationCategory.RANK,
        default_item="Champion Defeated",
        access_condition=AccessCondition(champion_data.get("requirements"))
    )

    LOCATIONS.add_location(f"{region_name}_Champion", rank_location)
    return rank_location


def add_encounter_data(encounter_data, region_name) -> EncounterData:
    encounter_id = encounter_data.get('id')
    encounter = EncounterData(
        encounter_id=encounter_id,
        encounter_name=f"{region_name}_{encounter_id}",
        is_champion=False,
        region=region_name,
        access_condition=AccessCondition(encounter_data.get("requirements"))
    )

    ENCOUNTERS.add_encounter(encounter, encounter_data.get("monsters"))

    return encounter


def add_champion_data(champion_data, region_name) -> EncounterData:
    encounter_id = champion_data.get('id')
    encounter = EncounterData(
        encounter_id=encounter_id,
        encounter_name=f"{region_name}_{encounter_id}",
        is_champion=True,
        region=region_name,
        access_condition=AccessCondition(champion_data.get("requirements"))
    )

    ENCOUNTERS.add_encounter(encounter, champion_data.get("monsters"))

    return encounter


def add_flag_data(flag_data, region_name) -> FlagData:
    event_flag = FlagData(
        location_name=flag_data["id"],
        item_name=flag_data["name"],
        region=region_name,
        access_condition=AccessCondition(flag_data.get("requirements"))
    )

    FLAGS.add_flag(event_flag)
    return event_flag

# endregion
