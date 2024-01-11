from typing import List, Dict

from BaseClasses import MultiWorld, Tutorial, ItemClassification, Entrance
from Options import Range, Toggle
from worlds.AutoWorld import World, WebWorld
from Utils import __version__

from . import data_importer
from . import regions as REGIONS
from . import items as ITEMS
from . import locations as LOCATIONS
from . import rules as RULES
from . import flags as FLAGS
from . import encounters as ENCOUNTERS

from .items import ItemData, MonsterSanctuaryItem, MonsterSanctuaryItemCategory
from .items import MonsterSanctuaryItemCategory as ItemCategory
from .locations import MonsterSanctuaryLocationCategory as LocationCategory, MonsterSanctuaryLocation, \
    MonsterSanctuaryLocationCategory, LocationData
from .options import MonsterSanctuaryOptions
from .regions import RegionData, MonsterSanctuaryRegion


class MonsterSanctuaryWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Monster Sanctuary with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["Saagael"]
    )]
    theme = "jungle"


def load_data():
    # Load the item and monster data from the json file so that we have access to it anywhere else
    item_id: int = 970500
    item_id = data_importer.load_items(item_id)
    item_id = data_importer.load_monsters(item_id)

    # Load the world second, since this will require having ItemData and MonsterData
    data_importer.load_world()
    data_importer.load_plotless()

    # We have to load flags last, as their location data is in world.json, but the item data exists in flags.json
    item_id = data_importer.load_flags(item_id)


class MonsterSanctuaryWorld(World):
    game = "Monster Sanctuary"
    web = MonsterSanctuaryWebWorld()
    options_dataclass = MonsterSanctuaryOptions
    options: MonsterSanctuaryOptions

    load_data()

    data_version = 0
    topology_present = True

    # Merge the monster ability groups and item groups
    item_name_groups = ITEMS.build_item_groups()
    for ability, monsters in ENCOUNTERS.build_explore_ability_groups().items():
        if item_name_groups[ability]:
            item_name_groups[ability].extend(monsters)
        else:
            item_name_groups[ability] = [monsters]

    item_name_to_id = {item.name: item.id for item in ITEMS.item_data.values()}
    location_name_to_id = {location.name: location.location_id
                           for location in LOCATIONS.location_data.values()}
    location_names = [location.name for location in LOCATIONS.location_data.values()]

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.number_of_item_locations = 0

    # is a class method called at the start of generation to check the existence of prerequisite files,
    # usually a ROM for games which require one.
    @classmethod
    def stage_assert_generate(cls, world: MultiWorld):
        pass

    # called per player before any items or locations are created. You can set properties on your world here.
    # Already has access to player options and RNG.
    def generate_early(self) -> None:
        pass

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # First, go through and create all the regions
        self.multiworld.regions += [
            MonsterSanctuaryRegion(self.multiworld, self.player, region_name)
            for region_name in REGIONS.region_data
        ]

        self.handle_plotless()
        self.create_item_locations()
        self.connect_regions()

    def handle_plotless(self):
        """Modifies connection, location, and flag rules if the skip_plot option is enabled"""
        if not self.options.skip_plot:
            return

        # Iterate over every plotless entry and replace the world graph data
        # with the plotless access condition
        for region_name in RULES.plotless_data:
            data = RULES.plotless_data[region_name]

            if data.type == "connection":
                region = REGIONS.region_data[region_name]
                conn = region.get_connection(data.connection)
                conn.access_rules = data.access_rules

            elif data.type == "location":
                location_name = f"{region_name}_{data.object_id}"
                location = LOCATIONS.location_data[location_name]
                location.access_condition = data.access_rules

            elif data.type == "flag":
                location = FLAGS.flag_data[data.id]
                location.access_condition = data.access_rules

    def create_item_locations(self) -> None:
        """Creates all locations for items, gifts, and rank ups"""
        for location_name in LOCATIONS.location_data:
            location_data = LOCATIONS.location_data[location_name]
            region = self.multiworld.get_region(location_data.region, self.player)

            location = MonsterSanctuaryLocation(
                self.player,
                location_data.name,
                location_data.location_id,
                region,
                location_data.access_condition or None)

            # if the goal is to defeat the mad lord, then
            # we do not add any post-game locations
            if self.options.goal == "defeat_mad_lord" and location_data.postgame:
                continue

            if location_data.category == MonsterSanctuaryLocationCategory.RANK:
                # Champion Defeated items are not shown in the spoiler log
                location.show_in_spoiler = False

            # Chest and Gift locations go here
            else:
                # Item locations can be filled with any item from another player, as well as items from this game
                location.item_rule = lambda item, loc = location: ITEMS.can_item_be_placed(item, loc)
                self.number_of_item_locations += 1

            region.locations.append(location)

    def connect_regions(self) -> None:
        """Connects all regions according to their access conditions"""
        for region_name in REGIONS.region_data:
            region_data = REGIONS.region_data[region_name]
            region = self.multiworld.get_region(region_name, self.player)

            for connection in region_data.connections:
                # If target region isn't defined, continue on.
                # This is because we haven't mapped out the whole world yet and some connections are placeholders
                target_region_data = REGIONS.region_data.get(connection.region)
                if target_region_data is None:
                    continue

                # Build the Entrance data
                connection_name = f"{region_data.name} to {connection.region}"
                entrance = Entrance(self.player, connection_name, region)
                # entrance.access_rule = connection.get_access_func(self.player)
                entrance.access_rule = lambda state, conn=connection: conn.access_rules.has_access(state, self.player)

                # Add it to the region's exits, and connect to the other region's entrance
                region.exits.append(entrance)
                entrance.connect(self.multiworld.get_region(connection.region, self.player))

    def set_victory_condition(self) -> None:
        if self.options.goal == "defeat_mad_lord":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Victory", self.player))

        elif self.options.goal == "defeat_all_champions":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Champion Defeated", self.player, 27))

    def place_ranks(self) -> None:
        """Creates the locations for rank ups, and locks Champion Defeated items to those locations"""
        for location_name in [location_name
                              for location_name in LOCATIONS.location_data
                              if LOCATIONS.location_data[location_name].category == MonsterSanctuaryLocationCategory.RANK]:

            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(self.create_item("Champion Defeated"))

    def place_events(self) -> None:
        """Creates locations for all flags, and places flag items at those locations"""
        for location_name, data in FLAGS.flag_data.items():
            region = self.multiworld.get_region(data.region, self.player)
            location = MonsterSanctuaryLocation(
                player=self.player,
                name=data.location_name,
                parent=region,
                access_condition=data.access_condition or None)

            if not hasattr(data, "item_id"):
                breakpoint()

            event_item = MonsterSanctuaryItem(self.player, data.item_id, data.item_name, data.item_classification)

            location.place_locked_item(event_item)
            region.locations.append(location)

    def place_locked_items(self):
        """Places items that need to be locked to a specific spot based on game options"""
        if self.options.randomize_monsters == "no":
            koi_location = self.multiworld.get_location("SunPalace_North2_20800117", self.player)
            koi_location.place_locked_item(self.create_item("Koi Egg"))

            bard_location = self.multiworld.get_location("ForgottenWorld_WandererRoom_45100110", self.player)
            bard_location.place_locked_item(self.create_item("Bard Egg"))

    def place_monsters(self) -> None:
        """Creates event locations for all monsters, and places monster items at those locations"""
        for encounter_name, encounter in ENCOUNTERS.encounter_data.items():
            region = self.multiworld.get_region(encounter.region, self.player)

            monster_index = 0
            for monster in encounter.monsters:
                location = MonsterSanctuaryLocation(
                    player=self.player,
                    name=f"{encounter.name}_{monster_index}",
                    parent=region,
                    access_condition=encounter.access_condition or None)
                location.show_in_spoiler = False

                monster_item = MonsterSanctuaryItem(
                    self.player,
                    monster.id,
                    monster.name,
                    ItemClassification.progression)

                location.place_locked_item(monster_item)
                region.locations.append(location)
                monster_index += 1

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        ITEMS.build_item_probability_table({
            MonsterSanctuaryItemCategory.CRAFTINGMATERIAL: self.options.drop_chance_craftingmaterial.value,
            MonsterSanctuaryItemCategory.CONSUMABLE: self.options.drop_chance_consumable.value,
            MonsterSanctuaryItemCategory.FOOD: self.options.drop_chance_food.value,
            MonsterSanctuaryItemCategory.CATALYST: self.options.drop_chance_catalyst.value,
            MonsterSanctuaryItemCategory.WEAPON: self.options.drop_chance_weapon.value,
            MonsterSanctuaryItemCategory.ACCESSORY: self.options.drop_chance_accessory.value,
            MonsterSanctuaryItemCategory.CURRENCY: self.options.drop_chance_currency.value,
        })
        pool: List[MonsterSanctuaryItem] = []

        # ITEMS
        # These items are not naturally put in the general item pool, and are handled separately
        item_exclusions = ["Multiple"]

        # Exclude relics of chaos if the option isn't enabled
        if self.options.include_chaos_relics:
            item_exclusions.append("Relic")

        # Add all key items to the pool
        key_items = [item_name for item_name in ITEMS.item_data
                     if ITEMS.item_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM]
        # Add items that are not technically key items, but are progressions items and should be added
        key_items.append("Raw Hide")
        key_items.append("Shard of Winter")
        key_items.append("Fire Stone")
        key_items.append("Ice Stone")
        key_items.append("Giant Seed")
        key_items.append("Dark Stone")
        key_items.append("Majestic Crown")
        key_items.append("Demonic Pact")
        key_items.append("Deep Stone")
        key_items.append("Primordial Branch")
        key_items.append("Druid Soul")

        # If monsters are not randomized, then we do not want to add Koi and Bard eggs to the pool
        # They will be locked to their original spot
        if self.options.randomize_monsters != "no":
            key_items.append("Koi Egg")
            key_items.append("Bard Egg")

        for key_item in key_items:
            for i in range(ITEMS.item_data[key_item].count):
                pool.append(self.create_item(key_item))

        while len(pool) < self.number_of_item_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                pool.append(self.create_item(item_name))

        self.multiworld.itempool += pool

    def create_item(self, item_name: str) -> MonsterSanctuaryItem:
        data = ITEMS.item_data.get(item_name)
        if data is None:
            raise KeyError(f"Item '{item_name}' has no data")
        return MonsterSanctuaryItem(self.player, data.id, item_name, data.classification)

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    # Rules are handled as AccessCondition objects within locations and connections
    def set_rules(self) -> None:
        pass

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        self.set_victory_condition()
        self.place_ranks()
        self.place_events()
        self.place_locked_items()

        ENCOUNTERS.randomize_monsters(self)
        self.place_monsters()

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    # def pre_fill(self):
    #     pass

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    # def fill_hook(self,
    #               progitempool: List["Item"],
    #               usefulitempool: List["Item"],
    #               filleritempool: List["Item"],
    #               fill_locations: List["Location"]) -> None:
    #     pass

    # called to modify item placement before, during and after the regular fill process, before generate_output.
    # If items need to be placed during pre_fill, these items can be determined and created using get_prefill_items
    # def post_fill(self):
    #     pass

    # creates the output files if there is output to be generated. When this is called,
    # self.multiworld.get_locations(self.player) has all locations for the player, with attribute
    # item pointing to the item. location.item.player can be used to see if it's a local item.
    def generate_output(self, output_directory: str) -> None:
        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "D:\\Visual Studio Projects\\Archipelago\\worlds\\monster_sanctuary\\world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        return {
            "exp_multiplier": self.options.exp_multiplier.value,
            "monsters_always_drop_egg": self.options.monsters_always_drop_egg.value,
            "monster_shift_rule": self.options.monster_shift_rule.value,
            "skip_intro": self.options.skip_intro.value,
            "skip_plot": self.options.skip_plot.value,
            "skip_battles": self.options.skip_battles.value
        }
