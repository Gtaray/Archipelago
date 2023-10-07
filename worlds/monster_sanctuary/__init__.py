from typing import List, Dict, Optional

from BaseClasses import MultiWorld, Tutorial, ItemClassification, Entrance
from Options import Range, Toggle
from worlds.AutoWorld import World, WebWorld

from . import data_importer
from . import regions as REGIONS
from . import items as ITEMS
from . import locations as LOCATIONS

from .items import ItemData, MonsterSanctuaryItem, MonsterSanctuaryItemCategory
from .items import MonsterSanctuaryItemCategory as ItemCategory
from .locations import MonsterSanctuaryLocationCategory as LocationCategory, MonsterSanctuaryLocation, \
    MonsterSanctuaryLocationCategory, LocationData
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

    load_data()

    data_version = 0
    topology_present = True

    item_name_groups = ITEMS.build_item_groups()
    item_name_to_id = {item.name: item.id for item in ITEMS.items_data.values()}
    location_name_to_id = {location.name: location.location_id
                           for location in LOCATIONS.locations_data.values()}
    location_names = [location.name for location in LOCATIONS.locations_data.values()]

    number_of_locations = 0

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
        for (option_name, option) in monster_sanctuary_options.items():
            result = getattr(self.multiworld, option_name)[self.player]
            if isinstance(result, Range):
                option_value = int(result)
            elif isinstance(result, Toggle):
                option_value = bool(result)
            else:
                option_value = result.current_key
            setattr(self, option_name, option_value)

    def shuffle_dictionary(self, dictionary) -> Dict:
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

    def connect_regions(self) -> None:
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

    def create_locations(self) -> None:
        for location_name in LOCATIONS.locations_data:
            location_data = LOCATIONS.locations_data[location_name]
            region = self.multiworld.get_region(location_data.region, self.player)
            location = MonsterSanctuaryLocation(
                self.player,
                location_data.name,
                location_data.location_id,
                region,
                location_data.access_condition or None)

            # if the goal is to defeat the mad lord, then
            # we do not add any post-game locations
            if self.goal == "defeat_mad_lord" and location_data.postgame:
                continue

            # Keep track of how many chest/gift location there are, because we need this count
            # to generate the correct number of filler items
            if (location_data.category == MonsterSanctuaryLocationCategory.GIFT
                    or location_data.category == MonsterSanctuaryLocationCategory.CHEST):
                self.number_of_locations += 1

            region.locations.append(location)

    def set_victory_condition(self) -> None:
        if self.goal == "defeat_mad_lord":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Victory", self.player))

        elif self.goal == "defeat_all_champions":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Champion Defeated", self.player, 27))

    def place_monsters(self) -> None:
        # This is used to keep track of monsters that have yet to be placed
        monsters: List[ItemData] = []

        # Used if the monster randomizer setting is set to "by specie"
        # This is a 1 to 1 map of one monster to another monster type
        shuffled_monsters: Dict[str, ItemData] = {}

        # this is used if the monster randomizer settings are set to "by encounter"
        # in which case we use this to store monster data by location name
        monsters_by_encounter: Dict[str, Dict[str, str]] = {}

        if self.randomize_monsters == "by_specie":
            # Globally maps monsters 1 to 1 with other monsters randomly
            # Every monster is guaranteed to show up. Though some monsters could be more
            # difficult to track down, such as Plague Egg, Skorch, champions, worm, etc.
            # This could mean that progression is gated behind finding one of these rare mons
            shuffled_monsters = self.shuffle_dictionary(ITEMS.get_monsters())

        elif self.randomize_monsters == "by_encounter" or self.randomize_monsters == "any":
            monsters = list(ITEMS.get_monsters().values())
            self.multiworld.random.shuffle(monsters)

        # Place monsters
        monster_locations: List[LocationData] = []

        # If champions are randomized using default monster rando rules
        # then we lump it in with these settings. The main reason we do this is so that the
        # normal and champion encounters can use the same by-encounter and shuffle lists
        if self.randomize_champions == "default":
            monster_locations = LOCATIONS.get_locations_of_type(LocationCategory.MONSTER, LocationCategory.CHAMPION)
        else:
            monster_locations = LOCATIONS.get_locations_of_type(LocationCategory.MONSTER)

        # Since we don't want to fill out a full list of monsters and shuffle that, we have to
        # shuffle the list of locations. This solves the issue where every monster shows up
        # exactly once in every 111 monster locations
        self.multiworld.random.shuffle(monster_locations)

        for location_data in monster_locations:
            # If we've placed all monsters in the list, then we refill the list again
            if len(monsters) == 0:
                monsters = list(ITEMS.get_monsters().values())
                self.multiworld.random.shuffle(monsters)

            location = self.multiworld.get_location(location_data.name, self.player)
            self.place_monster(location, monsters, shuffled_monsters, monsters_by_encounter)

    def place_monster(self, location, monsters, shuffled_monsters, monsters_by_encounter) -> None:
        data = LOCATIONS.locations_data[location.name]
        monster_name: str = data.default_item

        # TODO: Add a global list to pull from so that mons don't get re-used til all monsters have been placed
        # Don't need to add a case for no randomization, because the default item is used for monster_name above

        # When placing monsters, if the default item is Empty Slot, then we leave the location alone
        # This is because champion encounters frequently have only one monster, even though there are three slots
        # We need to keep three slots so that we can shuffle champion encounters around
        # The only reason a champion encounter gets into this function is because we're randomizing them
        # with default rules. If that's the case, then we leave the empty locations alone.
        if data.default_item == "Empty Slot":
            # We still want to create an "Empty Slot" item to fill the location with so that all locations are filled
            # and so it doesn't get filled with items. This if case is here as information to future readers
            pass

        # We already shuffled the monsters list above, so we just pull from it here
        elif self.randomize_monsters == "by_specie":
            monster_name = shuffled_monsters[data.default_item].name

        # if randomizing by encounter, every encounter maps monsters 1 to 1 with another monster
        elif self.randomize_monsters == "by_encounter":
            data = monsters.pop(0)

            if monsters_by_encounter.get(location.name) is None:
                monsters_by_encounter[data.object_id] = {}
            if monsters_by_encounter[data.object_id].get(data.default_item) is None:
                monsters_by_encounter[data.object_id][data.default_item] = data.name
            monster_name = monsters_by_encounter[data.object_id][data.default_item]

        # If nothing else, randomize the monster
        elif self.randomize_monsters == "any":
            data = monsters.pop(0)
            monster_name = data.name

        # create the item
        monster = self.create_item(monster_name)

        # Place the selected monster
        location.place_locked_item(monster)

    def place_champions(self) -> None:
        champions: Dict[str, List[str]] = LOCATIONS.get_champions()

        # Globally maps champion encounters 1 to 1 with other champion encounters
        if self.randomize_champions == "shuffle":
            champions = self.shuffle_dictionary(champions)

        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.CHAMPION:
                    self.place_champion(location, champions)

    def place_champion(self, location, champions) -> None:
        data = LOCATIONS.locations_data[location.name]
        monster_name: str = data.default_item

        # The default case it handled with the place_monsters() method.
        # We do this so that champions and normal battles
        # share the same monster randomization settings
        if self.randomize_champions == "default":
            return

        elif self.randomize_champions == "no" or self.randomize_champions == "shuffle":
            # Don't have to worry about Empty Slots here because they simply get shuffled around
            # with the rest of the encounter, and we handle the Empty Slot later in this method
            monster_name = champions[data.region][data.monster_id]

        # TODO: Probably add more detail to this?
        elif self.randomize_champions == "random":
            # Do not randomize any locations that would have an empty slot by default
            # This is so that champion encounters that normally only have one monster
            # remain with only a single monster
            if data.default_item != "Empty Slot":
                monster_name = ITEMS.get_random_monster_name(self.multiworld)

        # create the item
        # This will allow creating "Empty Slot" objects, which is fine
        # because the client will just ignore that data
        monster = self.create_item(monster_name)

        # Place the selected monster
        location.place_locked_item(monster)

    def place_keeper_battles(self) -> None:
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.KEEPER:
                    self.place_keeper_battle(location)

    def place_keeper_battle(self, location) -> None:
        data = LOCATIONS.locations_data[location.name]
        monster_name = ITEMS.get_random_monster_name(self.multiworld)
        monster = self.create_item(monster_name)

        # Monsters placed in keeper battles need to be marked as NOT progression
        monster.classification = ItemClassification.filler

        location.place_locked_item(monster)

    def place_ranks(self) -> None:
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.RANK:
                    rank_item = self.create_item("Champion Defeated")
                    location.place_locked_item(rank_item)

    def place_events(self) -> None:
        for region in self.multiworld.regions:
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]
                if data.category == LocationCategory.FLAG and location.item is None:
                    location.place_locked_item(self.create_item(data.default_item))

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        ITEMS.build_item_probability_table(self.multiworld, self)
        pool: List[MonsterSanctuaryItem] = []

        # These items are not naturally put in the general item pool, and are handled separately
        item_exclusions = ["Multiple"]

        # Exclude relics of chaos if the option isn't enabled
        if not self.include_chaos_relics:
            item_exclusions.append("Relic")

        # Add all key items to the pool
        key_items = [item_name for item_name in ITEMS.items_data
                     if ITEMS.items_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM]
        # Add items that are not technically key items, but are progressions items and should be added
        key_items.append("Raw Hide")
        key_items.append("Koi Egg")
        key_items.append("Bard Egg")
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

        for key_item in key_items:
            for i in range(ITEMS.items_data[key_item].count):
                pool.append(self.create_item(key_item))

        # TODO: Make a better way to fill the item pool
        while len(pool) < self.number_of_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                item = self.create_item(item_name)
                pool.append(item)

        self.multiworld.itempool += pool

    # create any item on demand
    def create_item(self, item_name: str) -> MonsterSanctuaryItem:
        data = ITEMS.items_data.get(item_name)
        if data is None:
            raise KeyError(f"Item '{item_name}' has no data")
        return MonsterSanctuaryItem(self.player, item_name, data)

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    def set_rules(self) -> None:
        pass

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        # Monsters are placed before items, with very little inherent logic. Items are them placed afterward
        # taking into account the locations of monsters and what explore abilities players will have access too
        self.set_victory_condition()
        self.place_monsters()
        self.place_champions()
        self.place_keeper_battles()
        self.place_ranks()
        self.place_events()

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
        visualize_regions(self.multiworld.get_region("Menu", self.player), "D:\\Downloads\\world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        print(self.monster_shift_rule)
        return {
            "exp_multiplier": self.exp_multiplier,
            "monsters_always_drop_egg": self.monsters_always_drop_egg,
            "monster_shift_rule": self.monster_shift_rule
        }
