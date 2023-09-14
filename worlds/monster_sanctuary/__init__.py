import settings

from typing import List

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld

from .items import item_table, MonsterSanctuaryItem
from .locations import location_table, MonsterSanctuaryLocationCategory
from .regions import create_regions
from .rules import set_rules
from .options import monstersanctuary_options


class MonsterSanctuaryWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Monster Sanctuary with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["Saagael"]
    )]


class MonsterSanctuaryWorld(World):
    game = "Monster Sanctuary"
    web = MonsterSanctuaryWebWorld()
    option_definitions = monstersanctuary_options

    data_version = 0

    topology_present = True

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    item_name_groups = items.build_item_groups()

    locations.build_location_ids()
    location_name_to_id = {location.name: location.id for location in location_table
                           if location.id is not None and location.category == MonsterSanctuaryLocationCategory.ITEM}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    # is a class method called at the start of generation to check the existence of prerequisite files,
    # usually a ROM for games which require one.
    @classmethod
    def stage_assert_generate(cls, world: MultiWorld):
        pass

    # called per player before any items or locations are created. You can set properties on your world here.
    # Already has access to player options and RNG.
    def generate_early(self) -> None:
        # Pull values in from settings to the world instance
        pass

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # This not only creates all the regions within the world
        # but assigns all locations to their respective regions
        create_regions(self.multiworld, self.player)

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterwards.
    def create_items(self) -> None:
        pass

    # create any item on demand
    def create_item(self, item: str) -> MonsterSanctuaryItem:
        return MonsterSanctuaryItem(item, item_table[item])

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        pass

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    def pre_fill(self):
        pass

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        pass

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    def post_fill(self):
        pass

    # creates the output files if there is output to be generated. When this is called,
    # self.multiworld.get_locations(self.player) has all locations for the player, with attribute
    # item pointing to the item. location.item.player can be used to see if it's a local item.
    def generate_output(self, output_directory: str):
        pass

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self):
        pass
