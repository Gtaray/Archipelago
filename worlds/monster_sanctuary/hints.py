from typing import Dict, Optional

from BaseClasses import ItemClassification, Item, Location
from worlds.AutoWorld import World

item_categories: Dict[ItemClassification, str] = {
    ItemClassification.filler: "useless",
    ItemClassification.useful: "useful",
    ItemClassification.trap: "valuable",  # It's a trap, so let's pretend it's a progression item
    ItemClassification.progression: "valuable",
    ItemClassification.skip_balancing: "useful",
    ItemClassification.progression_skip_balancing: "valuable",
}


class HintData:
    name: str
    id: int
    text: str
    ignore_other_text: bool
    item_name: Optional[str] = None
    item_location: Optional[str] = None

    def __init__(self, json_data):
        self.name = json_data["name"]
        self.id = json_data["id"]
        self.text = json_data["text"]
        self.ignore_other_text = json_data["ignore_other_text"]
        if "item_name" in json_data:
            self.item_name = json_data["item_name"]
        if "item_location" in json_data:
            self.item_location = json_data["item_location"]


class Hint:
    id: int
    text: str
    ignore_other_text: bool

    def __str__(self):
        return f"{self.id}: {self.text}"


hint_data: Dict[int, HintData] = {}


def generate_hints(world: World):
    world.hints = []

    # Get the items or locations we're hinting at
    location: Optional[Location] = None
    for hint_id, hintdata in hint_data.items():
        if hintdata.item_location is not None:
            location = world.multiworld.get_location(hintdata.item_location, world.player)
        if hintdata.item_name is not None:
            choices = world.multiworld.find_item_locations(hintdata.item_name, world.player)
            if len(choices) > 0:
                location = world.hint_rng.choice(choices)

        if location is None:
            continue

        hint = Hint()
        hint.id = hint_id
        hint.ignore_other_text = hintdata.ignore_other_text
        hint.text = (hintdata.text
                     .replace('{area}', get_area_name_for_location(location, world.player))
                     .replace('{category}', get_category_for_item(location.item))
                     .replace("{item}", f"{{{location.item.name}}}"))
        world.hints.append(hint)


def get_area_name_for_location(location: Location, player: int) -> str:
    if location.player != player:
        return "in another world"

    # converge item and monster location naming structures by getting rid of
    # spaces and converting hyphens to underscores
    area: str = location.name.replace(' ', '').replace('-', '_').split('_')[0]

    if area == "MountainPath":
        return "on the {Mountain Path}"
    elif area == "BlueCave":
        return "in the {Blue Caves}"
    elif area == "KeeperStronghold":
        return "in the {Keeper Stronghold}"
    elif area == "StrongholdDungeon":
        return "in the {Stronghold Dungeon}"
    elif area == "SnowyPeaks":
        return "on the {Snowy Peaks}"
    elif area == "SunPalace":
        return "in {Sun Palace}"
    elif area == "AncientWoods":
        return "in the {Ancient Woods}"
    elif area == "HorizonBeach":
        return "at {Horizon Beach}"
    elif area == "MagmaChamber":
        return "in the {Magma Chamber}"
    elif area == "BlobBurg":
        return "in {Blob Burg}"
    elif area == "Underworld":
        return "in the {Underworld}"
    elif area == "MysticalWorkshop":
        return "in the {Mystical Workshop}"
    elif area == "ForgottenWorld":
        return "in the {Forgotten World}"
    elif area == "AbandonedTower":
        return "in the {Abandoned Tower}"

    return "in an unknown location"


def get_category_for_item(item: Item) -> str:
    return f"{{{item_categories[item.classification]}}}"
