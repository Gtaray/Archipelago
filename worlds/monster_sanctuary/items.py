import math
from enum import IntEnum
from typing import List, Dict, Optional
from BaseClasses import ItemClassification
from BaseClasses import MultiWorld, Item
from worlds.AutoWorld import World


class MonsterSanctuaryItemCategory(IntEnum):
    KEYITEM = 0
    CRAFTINGMATERIAL = 1
    CONSUMABLE = 2
    FOOD = 3
    CATALYST = 4
    WEAPON = 5
    ACCESSORY = 6
    CURRENCY = 7
    EGG = 8
    MONSTER = 9,
    RANK = 10,
    FLAG = 11,
    COSTUME = 12


class ItemData:
    id: int
    name: str
    classification: ItemClassification
    category: MonsterSanctuaryItemCategory
    tier: Optional[int]
    unique: bool
    groups: List[str]
    count: int = 1  # how many of this item should be added to the game

    def __init__(self, item_id, name, classification, category, tier=None, unique=False, groups=None):
        self.id = item_id
        self.name = name
        self.classification = classification
        self.category = category
        self.tier = tier
        self.unique = unique

        if groups is not None:
            self.groups = groups
        else:
            self.groups = []


class MonsterSanctuaryItem(Item):
    game: str = "Monster Sanctuary"
    quantity: int = 1

    def __init__(self, player: int, name: str, data: ItemData):
        super(MonsterSanctuaryItem, self).__init__(name, data.classification, data.id, player)


# This holds all the item data that is parsed from items.json file
items_data: Dict[str, ItemData] = {}
item_drop_probabilities: List[MonsterSanctuaryItemCategory] = []


# region Monster Accessor functions
def get_monsters() -> Dict[str, ItemData]:
    return {item_name: items_data[item_name] for item_name in items_data
            if items_data[item_name].category is MonsterSanctuaryItemCategory.MONSTER
            and item_name not in ["Empty Slot",
                                  "Spectral Wolf",
                                  "Spectral Toad",
                                  "Spectral Eagle",
                                  "Spectral Lion",
                                  "Bard"]}


def get_random_monster_name(world: MultiWorld) -> str:
    valid_items = [item for item in get_monsters()]
    return world.random.choice(valid_items)
# endregion


def build_item_groups() -> Dict:
    item_groups = {}
    for item, data in items_data.items():
        for group in data.groups:
            item_groups[group] = item_groups.get(group, []) + [item]

    return item_groups


def is_in_item_pool(item: str, itempool: List[MonsterSanctuaryItem]) -> bool:
    """Checks to see if the item name is already in the item pool"""
    return item in [pool_item.name for pool_item in itempool]


def is_item_in_group(item: str, *groups: str) -> bool:
    """Checks to see fi the item is in any of the given groups"""
    # If there's on groups to check, then we return true
    if len(groups) == 0:
        return True
    return not set(items_data[item].groups).isdisjoint(groups)


def get_item_type(item_name: str) -> Optional[MonsterSanctuaryItemCategory]:
    item = items_data.get(item_name)
    if item is None:
        return None

    return item.category


def is_item_type(item_name: str, item_type: MonsterSanctuaryItemCategory) -> bool:
    return get_item_type(item_name) == item_type


def get_item_tier(item_name: str) -> Optional[int]:
    item = items_data.get(item_name)
    if item is None:
        return None

    return item.tier


def is_item_tier(item: str, tier: int) -> bool:
    return get_item_tier(item) == tier


def get_filtered_unique_item_data(itempool: List[MonsterSanctuaryItem]) -> Dict[str, ItemData]:
    """Given a list of items, this returns a subset of that list with unique items removed
    if the unique item is already in the item pool"""
    return {item: items_data[item] for item in items_data
            if not items_data[item].unique
            or not is_in_item_pool(item, itempool)}


def build_item_probability_table(multiworld: MultiWorld, world: World) -> None:
    probabilities = {
        MonsterSanctuaryItemCategory.CRAFTINGMATERIAL: world.drop_chance_craftingmaterial,
        MonsterSanctuaryItemCategory.CONSUMABLE: world.drop_chance_consumable,
        MonsterSanctuaryItemCategory.FOOD: world.drop_chance_food,
        MonsterSanctuaryItemCategory.CATALYST: world.drop_chance_catalyst,
        MonsterSanctuaryItemCategory.WEAPON: world.drop_chance_weapon,
        MonsterSanctuaryItemCategory.ACCESSORY: world.drop_chance_accessory,
        MonsterSanctuaryItemCategory.CURRENCY: world.drop_chance_currency,
    }

    for item_type in probabilities:
        for i in range(probabilities[item_type]):
            item_drop_probabilities.append(item_type)


def get_random_item_name(world: World,
                         itempool: List[MonsterSanctuaryItem],
                         group_include: Optional[List[str]] = None,
                         group_exclude: Optional[List[str]] = None) -> Optional[str]:
    """Gets a random item name from the master item list with the following restrictions:
    Unique items already in the item pool will not be added a second time
    Items with groups that intersect with group_exclude will not be added
    Only items whose groups intersect with group_include will be selected from"""

    if group_include is None:
        group_include = []
    if group_exclude is None:
        group_exclude = []

    # We should never return multiple items, those require special randomization
    # that happens down below
    if "Multiple" not in group_exclude:
        group_exclude.append("Multiple")

    item_type = world.multiworld.random.choice(item_drop_probabilities)
    valid_items = [item for item in get_filtered_unique_item_data(itempool)
                   if is_item_type(item, item_type)
                   and is_item_in_group(item, *group_include)
                   and not is_item_in_group(item, *group_exclude)]

    if len(valid_items) == 0:
        return None

    base_item_name = world.multiworld.random.choice(valid_items)
    base_item = items_data.get(base_item_name)

    name_prepend = None
    if "Up to 2" in base_item.groups:
        roll = world.multiworld.random.randint(1, 10)
        if roll >= 7:
            name_prepend = "2x"
    elif "Up to 3" in base_item.groups:
        roll = world.multiworld.random.randint(1, 10)
        if roll >= 9:
            name_prepend = "3x"
        elif roll >= 6:
            name_prepend = "2x"
    elif "Up to 4" in base_item.groups:
        roll = world.multiworld.random.randint(1, 10)
        if roll >= 10:
            name_prepend = "4x"
        elif roll >= 8:
            name_prepend = "2x"
        elif roll >= 5:
            name_prepend = "2x"

    if name_prepend is not None:
        new_item_name = f"{name_prepend} {base_item_name}"
        if new_item_name is not None and items_data.get(new_item_name) is not None:
            base_item_name = new_item_name

    return base_item_name
