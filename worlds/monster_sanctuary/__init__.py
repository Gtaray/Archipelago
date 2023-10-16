from typing import List, Dict

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

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        # Tracks which monsters have been placed as champions, so that we don't re-use them
        self.champions_used: List[str] = []

        # Handles shuffled and default settings for champions
        self.champion_data: Dict[str, List[str]] = LOCATIONS.get_champions()

        # Generic list of all available monsters. Can be modified by shuffling,
        # or by removing champions/evolved mons from the list
        self.monsters: Dict[str, ItemData] = ITEMS.get_monsters()

        self.number_of_item_locations = 0
        self.number_of_monster_locations = 0

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

        # We have to do this early so that the lists are set up for when we create locations
        self.prepare_monster_lists()

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

        self.create_locations()
        self.connect_regions()

    def connect_regions(self) -> None:
        for region_name in REGIONS.regions_data:
            region_data = REGIONS.regions_data[region_name]
            region = self.multiworld.get_region(region_name, self.player)

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

            if location_data.category == MonsterSanctuaryLocationCategory.CHAMPION:
                champion = self.create_item(self.champion_data[region.name][location_data.monster_id])
                location.place_locked_item(champion)

            if location_data.category == MonsterSanctuaryLocationCategory.MONSTER:
                self.number_of_monster_locations += 1
                location.item_rule = lambda item: (
                        item.player == location.player and
                        ITEMS.items_data[item.name].category == MonsterSanctuaryItemCategory.MONSTER)

            # Item and gift locations CANNOT contain monsters
            if (location_data.category == MonsterSanctuaryLocationCategory.GIFT
                    or location_data.category == MonsterSanctuaryLocationCategory.CHEST):
                location.item_rule = lambda item: (not ITEMS.is_item_type(item.name,
                                                                          MonsterSanctuaryItemCategory.RANK,
                                                                          MonsterSanctuaryItemCategory.MONSTER,
                                                                          MonsterSanctuaryItemCategory.FLAG))
                self.number_of_item_locations += 1

            region.locations.append(location)

    def set_victory_condition(self) -> None:
        if self.goal == "defeat_mad_lord":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Victory", self.player))

        elif self.goal == "defeat_all_champions":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Champion Defeated", self.player, 27))

    def prepare_monster_lists(self) -> None:
        # We start by shuffling the champion dictionary, if necessary
        if self.randomize_champions == "shuffle":
            self.champion_data = self.shuffle_dictionary(self.champion_data)

        # In this case, we randomize champions to literally anything
        elif self.randomize_champions == "any":
            for region_name in self.champion_data:
                for i in range(len(self.champion_data[region_name])):
                    if self.champion_data[region_name][i] == "Empty Slot":
                        continue
                    self.champion_data[region_name][i] = ITEMS.get_random_monster_name(self.multiworld)

        # After setting the champion data above, we go through and add those monsters to the 'used'
        # in case the 'champions don't appear in the wild' option is enabled.
        for region_name in self.champion_data:
            # For champion fights with more than one monster, we always take the middle one
            # which is the second element in the array.
            # Champion fights with 1 monster, we take the first element (obviously)
            if self.champion_data[region_name][1] == "Empty Slot":
                self.champions_used.append(self.champion_data[region_name][0])
            else:
                self.champions_used.append(self.champion_data[region_name][1])

        # Remove evolutions from encounter pool if necessary
        if not self.evolutions_in_wild:
            del self.monsters["G'rulu"]
            del self.monsters["Magmamoth"]
            del self.monsters["Megataur"]
            del self.monsters["Ninki Nanka"]
            del self.monsters["Sizzle Knight"]
            del self.monsters["Silvaero"]
            del self.monsters["Glowdra"]
            del self.monsters["Dracogran"]
            del self.monsters["Dracozul"]
            del self.monsters["Mega Rock"]
            del self.monsters["Draconoir"]
            del self.monsters["King Blob"]
            del self.monsters["Mad Lord"]
            del self.monsters["Ascendant"]
            del self.monsters["Fumagus"]
            del self.monsters["Dracomer"]

        # Lastly, if we don't want champions to show up in the wild,
        if self.champions_in_wild:
            for champion in self.champions_used:
                if self.monsters.get(champion) is not None:
                    del self.monsters[champion]

    def place_champions(self) -> None:
        for location in [location_name
                         for location_name in LOCATIONS.locations_data
                         if LOCATIONS.locations_data[location_name].category == MonsterSanctuaryLocationCategory.CHAMPION]:
            self.place_champion(location)

    def place_champion(self, location_name: str) -> None:
        data = LOCATIONS.locations_data[location_name]
        monster_name: str = self.champion_data[data.region][data.monster_id]

        monster = self.create_item(monster_name)

        location = self.multiworld.get_location(location_name, self.player)
        location.place_locked_item(monster)

    def place_keeper_battles(self) -> None:
        for region in self.multiworld.get_regions(self.player):
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
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]

                if data.category == LocationCategory.RANK:
                    rank_item = self.create_item("Champion Defeated")
                    location.place_locked_item(rank_item)

    def place_events(self) -> None:
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                data = LOCATIONS.locations_data[location.name]
                if data.category == LocationCategory.FLAG and location.item is None:
                    location.place_locked_item(self.create_item(data.default_item))

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        ITEMS.build_item_probability_table(self)
        pool: List[MonsterSanctuaryItem] = []

        # ITEMS
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

        while len(pool) < self.number_of_item_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                pool.append(self.create_item(item_name))

        self.multiworld.itempool += pool

        # MONSTERS
        pool = []  # Re-set the temp item pool to empty

        for monster in self.monsters:
            pool.append(self.create_item(monster))

        monster_names = list(self.monsters.keys())
        while len(pool) < self.number_of_monster_locations:
            monster_name = self.multiworld.random.choice(monster_names)
            pool.append(self.create_item(monster_name))

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
        # self.place_champions()
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
        pass
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "D:\\Downloads\\world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        print(self.monster_shift_rule)
        return {
            "exp_multiplier": self.exp_multiplier,
            "monsters_always_drop_egg": self.monsters_always_drop_egg,
            "monster_shift_rule": self.monster_shift_rule,
            "skip_intro": self.skip_intro
        }
