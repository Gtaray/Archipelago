from typing import List, Set, Dict, Optional

import Utils
from BaseClasses import Item, MultiWorld, Tutorial, Location, ItemClassification, Entrance
from Options import Range, Toggle, VerifyKeys
from worlds.AutoWorld import World, WebWorld

from . import data_importer
from . import regions as REGIONS
from . import items as ITEMS
from . import locations as LOCATIONS

from .items import ItemData,MonsterSanctuaryItem
from .items import MonsterSanctuaryItemCategory as ItemCategory
from .locations import MonsterSanctuaryLocationCategory as LocationCategory, MonsterSanctuaryLocation
from .options import monster_sanctuary_options
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
    # Load the item data from the json file so that we have access to it anywhere else
    data_importer.load_world()
    data_importer.load_items()


class MonsterSanctuaryWorld(World):
    game = "Monster Sanctuary"
    web = MonsterSanctuaryWebWorld()
    option_definitions = monster_sanctuary_options

    data_version = 0
    topology_present = True

    item_name_groups = {}
    item_name_to_id = {}
    location_name_to_id = {}

    def __init__(self, world: MultiWorld, player: int):
        load_data()

        MonsterSanctuaryWorld.item_name_groups = ITEMS.build_item_groups()
        MonsterSanctuaryWorld.item_name_to_id = {item.name: item.id for item in ITEMS.items_data.values()}
        MonsterSanctuaryWorld.location_name_to_id = {location.name: location.location_id for location in locations.locations_data.values()}

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
        for (option_name, option) in monster_sanctuary_options.items():
            result = getattr(self.multiworld, option_name)[self.player]
            if isinstance(result, Range):
                option_value = int(result)
            elif isinstance(result, Toggle):
                option_value = bool(result)
            else:
                option_value = result.current_key
            setattr(self, option_name, option_value)

    def shuffle_dictionary(self, dictionary):
        keys = list(dictionary.keys())
        values = list(dictionary.values())
        self.multiworld.random.shuffle(values)

        # After shuffling the ItemData, we map those now shuffled items
        # back onto the dictionary
        for i in range(len(keys)):
            dictionary[keys[i]] = values[i]

        return dictionary

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # First, go through and create all the regions
        for region_name in REGIONS.regions_data:
            region = MonsterSanctuaryRegion(self.multiworld, self.player, region_name)
            self.multiworld.regions += [region]

        self.connect_regions()
        self.create_locations()

    def connect_regions(self):
        for region in self.multiworld.regions:
            region_data = REGIONS.regions_data[region.name]

            for connection in region_data.connections:
                # If target region isn't defined, continue on.
                # This is because we haven't mapped out the whole world yet and some connections are placeholders
                target_region_data = REGIONS.regions_data.get(connection.region)
                if target_region_data is None:
                    continue

                # Build the Entrance data
                connection_name = f"{region_data.name} to {connection.region}"
                entrance = Entrance(self.player, connection_name, region)
                # entrance.access_rule = connection.get_access_func(self.player)
                entrance.access_rule = lambda state, conn=connection: conn.access_rules.has_access(state, self.player)

                # Add it to the region's exist, and connect to the other region's entrance
                region.exits.append(entrance)
                entrance.connect(self.multiworld.get_region(connection.region, self.player))

    def create_locations(self):
        for location_name in LOCATIONS.locations_data:
            location_data = LOCATIONS.locations_data[location_name]
            region = self.multiworld.get_region(location_data.region, self.player)
            region.locations += [MonsterSanctuaryLocation(
                self.player,
                location_data.name,
                location_data.location_id,
                region,
                location_data.access_condition)]

    def place_monsters(self):
        monsters: Dict[str, ItemData] = ITEMS.get_monsters()

        # this is used if the monster randomizer settings are set to "by encounter"
        # in which case we use this to store monster data by location name
        monsters_by_encounter: Dict[str, Dict[str, str]] = {}

        # Globally maps monsters 1 to 1 with other monsters randomly
        if self.randomize_monsters == "by_specie":
            monsters = self.shuffle_dictionary(monsters)

        # Place monsters
        print("Placing Monsters")
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                # If champions are randomized using default monster rando rules
                # then we lump it in with these settings. The main reason we do this is so that the
                # normal and champion encounters can use the same by-encounter and shuffle lists
                if (data.category == LocationCategory.MONSTER or
                        (data.category == LocationCategory.CHAMPION and self.randomize_champions == "default")):
                    self.place_monster(location, monsters, monsters_by_encounter)

    def place_monster(self, location, monsters, monsters_by_encounter):
        data = LOCATIONS.locations_data[location.name]
        monster_name: Optional[str] = None

        # When placing monsters, if the default item is None, then we lock the location and move on
        # this is because champion encounters frequently have only one monster, even though there are three slots
        # and we need to keep three slots because we can shuffle champion encounters around
        # The only reason champion encounters get into this function is because we're randomizing them
        # with default rules. If that's the case, then we leave the empty locations alone.
        if data.default_item is None:
            location.locked = True
            return

        # TODO: Add a global list to pull from so that mons don't get re-used til all monsters have been placed
        # Not randomizing monsters, so we put the default monster back in its location
        if self.randomize_monsters == "no":
            monster_name = data.default_item

        # We already shuffled the monsters list above, so we just pull from it here
        elif self.randomize_monsters == "by_specie":
            monster_name = monsters[data.default_item].name

        # if randomizing by encounter, every encounter maps monsters 1 to 1 with another monster
        elif self.randomize_monsters == "by_encounter":
            if monsters_by_encounter.get(location.name) is None:
                monsters_by_encounter[data.encounter_id] = {}
            if monsters_by_encounter[data.encounter_id].get(data.default_item) is None:
                monsters_by_encounter[data.encounter_id][
                    data.default_item] = items.get_random_monster_name(self.multiworld)
            monster_name = monsters_by_encounter[data.encounter_id][data.default_item]

        # If nothing else, randomize the monster
        else:
            monster_name = items.get_random_monster_name(self.multiworld)

        if monster_name is None:
            return

        # create the item
        monster = self.create_item(monster_name)

        # Place the selected monster
        location.place_locked_item(monster)

        # print(f"{location.name}: {data.default_item} -> {monster_name}")

    def place_champions(self):
        champions: Dict[str, List[str]] = LOCATIONS.get_champions()

        # Globally maps champion encounters 1 to 1 with other champion encounters
        if self.randomize_champions == "shuffle":
            champions = self.shuffle_dictionary(champions)

        print("Placing Champions")
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.CHAMPION:
                    self.place_champion(location, champions)

    def place_champion(self, location, champions):
        data = LOCATIONS.locations_data[location.name]
        monster_name: Optional[str] = None

        if self.randomize_champions == "no" or self.randomize_champions == "shuffle":
            monster_name = champions[data.region][data.monster_id]

        # We should never hit this, because the default case it handled
        # with the place_monsters() function. We do this so that champions and normal battles
        # share the same monster randomization settings, like shuffle
        elif self.randomize_champions == "default":
            pass

        # TODO: Probably add more detail to this?
        elif self.randomize_champions == "random":
            monster_name = items.get_random_monster_name(self.multiworld)

        # if the monster name is empty, we lock the location and move on
        # This occurs because all champion encounters have three monster slots,
        # but 2 are empty in a lot of cases.
        if monster_name is None:
            location.item_rule = lambda item: False
            return

        # create the item
        monster = self.create_item(monster_name)

        # Place the selected monster
        location.place_locked_item(monster)

    def place_keeper_battles(self):
        # Place monsters
        print("Placing Keeper Battles")
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.KEEPER:
                    self.place_keeper_battle(location)

    def place_keeper_battle(self, location):
        data = LOCATIONS.locations_data[location.name]
        monster_name = items.get_random_monster_name(self.multiworld)
        monster = self.create_item(monster_name)

        # Monsters placed in keeper battles need to be marked as NOT progression
        monster.classification = ItemClassification.filler

        location.place_locked_item(monster)

    def place_ranks(self):
        print("Placing Ranks")
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.RANK:
                    rank_item = self.create_item("Champion Defeated")
                    location.place_locked_item(rank_item)

    def place_events(self):
        print("Placing Flags")
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]
                if data.category == LocationCategory.FLAG:
                    print(f"Placing flag '{data.default_item}' in {data.name}")
                    location.place_locked_item(self.create_item(data.default_item))

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        # Monsters are placed before items, with very little inherent logic. Items are them placed afterward
        # taking into account the locations of monsters and what explore abilities players will have access too
        self.place_monsters()
        self.place_champions()
        self.place_keeper_battles()
        self.place_ranks()
        self.place_events()

        pool: list[MonsterSanctuaryItem] = []

        loc_count = len([loc for loc in LOCATIONS.locations_data if LOCATIONS.locations_data[loc].category == LocationCategory.CHEST or LOCATIONS.locations_data[loc].category == LocationCategory.GIFT])
        print(f"Number of Location: {loc_count}")

        # These items are not naturally put in the general item pool, and are handled separately
        item_exclusions = ["Multiple"]

        # Exclude relics of chaos if the option isn't enabled
        if not self.include_chaos_relics:
            item_exclusions.append("Relic")

        for location_name in LOCATIONS.locations_data:
            location = LOCATIONS.locations_data[location_name]

            # Monsters and champions are placed earlier
            if not (location.category == LocationCategory.CHEST
                    or location.category == LocationCategory.GIFT):
                continue

            # If this location contains a key item, add it and move on.
            # This should handle key items that show up multiple times
            if ITEMS.is_item_type(location.default_item, ItemCategory.KEYITEM):
                pool += [self.create_item(location.default_item)]
                continue

            item_tier = None

            # Match tier
            # This might not work long-term. We need to make sure items get put in chests
            # whose default item matches their tier, and this needs to happen after
            # key items are placed
            # This might end up with a mismatch in the number of items and locations of each tier
            # in which case we just need to fill with whatever item we can?
            # or we need to dynamically swap out items in the item pool if that's possible.
            if self.randomize_items == "by_tier":
                item_tier = items.get_item_tier(location.default_item)

            item_name = items.get_random_item_name(self, pool,
                                                   required_tier=item_tier,
                                                   group_exclude=item_exclusions)

            # This will break if any item returns None because
            # the itempool count will not match the location count
            if item_name is not None:
                item = self.create_item(item_name)
                pool += [item]

            # print(location.default_item + " -> " + item_name)
        self.multiworld.itempool += pool

    # create any item on demand
    def create_item(self, item_name: str) -> MonsterSanctuaryItem:
        return MonsterSanctuaryItem(self.player, item_name, items.items_data[item_name])

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    def set_rules(self) -> None:
        pass

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        pass

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
    def generate_output(self, output_directory: str):
        pass
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "D:\\Downloads\\world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self):
        pass
