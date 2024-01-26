import threading
import types
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
from . import hints as HINTS
from .encounters import MonsterData

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
    data_importer.load_hints()

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

    item_name_groups = ITEMS.build_item_groups()
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
        ENCOUNTERS.randomize_monsters(self)

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # First, go through and create all the regions
        self.multiworld.regions += [
            MonsterSanctuaryRegion(self.multiworld, self.player, region_name)
            for region_name in REGIONS.region_data
        ]

        self.create_item_locations()
        self.connect_regions()

        # These create locations and place items at those locations.
        # Needs to be done after location creation but before item placement
        self.place_events()
        self.handle_monster_eggs()
        self.place_monsters()

    def create_item_locations(self) -> None:
        """Creates all locations for items, gifts, and rank ups"""
        for location_name in LOCATIONS.location_data:
            location_data = LOCATIONS.location_data[location_name]

            # if the goal is to defeat the mad lord, then
            # we do not add any post-game locations
            if self.options.goal == "defeat_mad_lord" and location_data.postgame:
                continue

            # First we check if we should be ignoring these locations based on rando options
            # If we're never allowing shifting, then these locations should not be included, as they
            # require a shifted monster to get.
            if self.options.monster_shift_rule == "never" and location_data.name in [
                "Snowy Peaks - Cryomancer 2",
                "Snowy Peaks - Cryomancer 3",
                "Snowy Peaks - Cryomancer 4"
            ]:
                continue

            region = self.multiworld.get_region(location_data.region, self.player)

            plotless_rules = RULES.get_plotless_location(region.name, location_data.object_id)
            access_condition = location_data.access_condition or None
            if self.options.skip_plot and plotless_rules is not None:
                access_condition = plotless_rules.access_rules

            location = MonsterSanctuaryLocation(
                self.player,
                location_data.name,
                location_name,
                location_data.location_id,
                region,
                access_condition)

            if location_data.category == MonsterSanctuaryLocationCategory.RANK:
                # Champion Defeated items are not shown in the spoiler log
                location.show_in_spoiler = False

            # Chest and Gift locations go here
            else:
                # Item locations can be filled with any item from another player, as well as items from this game
                location.item_rule = lambda item, world = self, loc = location: ITEMS.can_item_be_placed(world, item, loc)
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

                plotless_rules = RULES.get_plotless_connection(region.name, target_region_data.name)
                access_condition = connection.access_rules or None
                if self.options.skip_plot and plotless_rules is not None:
                    access_condition = plotless_rules.access_rules

                # Build the Entrance data
                connection_name = f"{region_data.name} to {connection.region}"
                entrance = Entrance(self.player, connection_name, region)
                entrance.access_rule = lambda state, rules=access_condition: rules.has_access(state, self.player)

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
        for location_name in [loc.name
                              for name, loc in LOCATIONS.location_data.items()
                              if LOCATIONS.location_data[name].category == MonsterSanctuaryLocationCategory.RANK]:

            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(self.create_item("Champion Defeated"))

    def place_events(self) -> None:
        """Creates locations for all flags, and places flag items at those locations"""
        for location_name, data in FLAGS.flag_data.items():
            region = self.multiworld.get_region(data.region, self.player)

            plotless_rules = RULES.get_plotless_flag(region.name, data.location_name)
            access_condition = data.access_condition or None
            if self.options.skip_plot and plotless_rules is not None:
                access_condition = plotless_rules.access_rules

            location = MonsterSanctuaryLocation(
                player=self.player,
                name=data.location_name,
                logical_name=location_name,
                parent=region,
                access_condition=access_condition)

            if not hasattr(data, "item_id"):
                breakpoint()

            event_item = MonsterSanctuaryItem(
                self.player,
                data.item_id,
                data.item_name,
                data.item_classification)

            location.place_locked_item(event_item)
            region.locations.append(location)

    def handle_monster_eggs(self):
        eggs = {}

        if self.options.randomize_monsters == "by_specie":
            # These eggs either get added to the item pool or they are placed in their respective gift location
            eggs["Sun Palace - Caretaker 1"] = self.create_item(self.species_swap["Koi"].egg_name())
            # We never actually species swap Bard, so this is a bit redundant, but having it here makes it
            # clear that it should be handled here even if we did swap it
            eggs["Forgotten World - Wanderer Room"] = self.create_item(self.species_swap["Bard"].egg_name())
            eggs["Magma Chamber - Bex"] = self.create_item(self.species_swap["Skorch"].egg_name())
            eggs["Snowy Peaks - Cryomancer 1"] = self.create_item(self.species_swap["Shockhopper"].egg_name())
            eggs["Snowy Peaks - Cryomancer 2"] = self.create_item(self.species_swap["Shockhopper"].egg_name())
            eggs["Snowy Peaks - Cryomancer 3"] = self.create_item(self.species_swap["Shockhopper"].egg_name())
            # eggs["AlchemistShop_5"] = self.create_item(self.species_swap["Plague Egg"].egg_name()),

            # These are straight up added because they don't come from a specific location
            # they just need to be available in the pool somewhere to make sure all locations
            # are reachable.
            self.multiworld.itempool += [
                self.create_item(self.species_swap["Mad Lord"].egg_name()),
                self.create_item(self.species_swap["Plague Egg"].egg_name()),
                self.create_item(self.species_swap["Ninki"].egg_name()),
                self.create_item(self.species_swap["Sizzle Knight"].egg_name()),
                self.create_item(self.species_swap["Tanuki"].egg_name()),
            ]
            self.number_of_item_locations -= 5

        else:
            # These are monsters that are normally given through gifts, and are either added to the pool
            # or are locked at their original location
            eggs["Sun Palace - Caretaker 1"] = self.create_item("Koi Egg")
            eggs["Forgotten World - Wanderer Room"] = self.create_item("Bard Egg")
            eggs["Magma Chamber - Bex"] = self.create_item("Skorch Egg")
            eggs["Snowy Peaks - Cryomancer 1"] = self.create_item("Shockhopper Egg")
            eggs["Snowy Peaks - Cryomancer 2"] = self.create_item("Shockhopper Egg")
            eggs["Snowy Peaks - Cryomancer 3"] = self.create_item("Shockhopper Egg")

        # Depending on the options, these eggs are either added to the pool, or locked
        # into their default location
        if self.options.add_gift_eggs_to_pool:
            self.multiworld.itempool += list(item for location, item in eggs.items())
        else:
            for location, item in eggs.items():
                self.multiworld.get_location(location, self.player).place_locked_item(item)

        self.number_of_item_locations -= len(eggs)

    def place_monsters(self) -> None:
        """Creates event locations for all monsters, and places monster items at those locations"""
        for encounter_name, encounter in self.encounters.items():
            region = self.multiworld.get_region(encounter.region, self.player)

            monster_index = 0
            for monster in encounter.monsters:
                location = MonsterSanctuaryLocation(
                    player=self.player,
                    name=f"{encounter.name}_{monster_index}",
                    logical_name=f"{encounter.name}_{monster_index}",
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

        for key_item in key_items:
            item_count = ITEMS.item_data[key_item].count
            is_key = ITEMS.is_item_in_group(key_item, "Area Key")

            if is_key:
                if self.options.remove_locked_doors == "all":
                    # If we're opening all doors, then we never place area keys in the pool
                    continue
                elif self.options.remove_locked_doors == "minimal":
                    # If we're opening some doors, then we modify the number of keys placed
                    if key_item == "Ancient Woods key":
                        item_count = 2
                    elif key_item == "Mystical Workshop key":
                        item_count = 3
                    else:
                        item_count = 1

            for i in range(item_count):
                pool.append(self.create_item(key_item))

        while len(pool) < self.number_of_item_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                pool.append(self.create_item(item_name))

        self.multiworld.itempool += pool

    def create_item(self, item_name: str) -> MonsterSanctuaryItem:
        data = ITEMS.item_data.get(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.id, item_name, data.classification)

        data = ENCOUNTERS.monster_data.get(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.id, data.name, ItemClassification.progression)

        data = FLAGS.get_flag_by_item_name(item_name)
        if data is not None:
            return MonsterSanctuaryItem(self.player, data.item_id, data.item_name, data.item_classification)

        raise KeyError(f"Item '{item_name}' has no data")

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    # Rules are handled as AccessCondition objects within locations and connections
    def set_rules(self) -> None:
        if self.options.local_area_keys:
            self.options.local_items.value |= self.item_name_groups["Area Key"]

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        self.set_victory_condition()
        self.place_ranks()

    # creates the output files if there is output to be generated. When this is called,
    # self.multiworld.get_locations(self.player) has all locations for the player, with attribute
    # item pointing to the item. location.item.player can be used to see if it's a local item.
    def generate_output(self, output_directory: str) -> None:
        if self.options.hints:
            self.hint_rng = self.multiworld.per_slot_randoms[self.player]
            HINTS.generate_hints(self)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player),
                          "D:\\Visual Studio Projects\\Archipelago\\worlds\\monster_sanctuary\\world.puml")

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        slot_data = {}

        # Rando options
        slot_data["options"] = {
            "exp_multiplier": self.options.exp_multiplier.value,
            "monsters_always_drop_egg": self.options.monsters_always_drop_egg.value,
            "monster_shift_rule": self.options.monster_shift_rule.value,
            "skip_intro": self.options.skip_intro.value,
            "skip_plot": self.options.skip_plot.value,
            "remove_locked_doors": self.options.remove_locked_doors.value,
            "death_link": self.options.death_link.value
        }

        # Monster reandos
        tanuki_location = self.multiworld.get_location("Menu_0_0", self.player)
        slot_data["monsters"] = {
            "tanuki": tanuki_location.item.name,
        }

        # If we're shuffling monsters, then we want to show what Bex and the Caretaker's monsters are
        # so the player knows if they are needed for progression
        if self.options.randomize_monsters == "by_specie":
            slot_data["monsters"]["bex_monster"] = self.species_swap["Skorch"].name

        slot_data["monsters"]["monster_locations"] = {}
        slot_data["monsters"]["champions"] = {}
        for encounter_name, encounter in self.encounters.items():
            parts = encounter_name.split('_')

            # location names for monsters need to be without the subsection, so we only
            # take the first two parts of the name, then append the monster id
            location_name_base = f"{parts[0]}_{parts[1]}_{encounter.encounter_id}"
            for i in range(len(encounter.monsters)):
                location_name = f"{location_name_base}_{i}"
                slot_data["monsters"]["monster_locations"][location_name] = encounter.monsters[i].name

            if encounter.champion:
                # Monster is either the first and only mon, or the second mon
                monster = encounter.monsters[0]
                i = 0
                if len(encounter.monsters) > 1:
                    monster = encounter.monsters[1]
                    i = 1
                # We only need the scene name to be able to map champions
                slot_data["monsters"]["champions"][f"{parts[0]}_{parts[1]}"] = monster.name

        slot_data["locations"] = {}
        for location in self.multiworld.get_locations(self.player):
            region = location.parent_region
            if region.name.startswith("Menu"):  # Ignore menu locations
                continue
            if '_' in location.name:  # Ignore monster locations and flags
                continue
            if location.item.code is None:  # Ignore events
                continue

            name = LOCATIONS.get_location_name_for_client(location.logical_name)
            if name is None:
                continue

            area = region.name.split("_")[0]
            if area not in slot_data["locations"]:
                slot_data["locations"][area] = {}
            slot_data["locations"][area][name] = location.address

        if self.options.hints:
            # There's probably a much better way of doing this.
            # I just want an anonymous object that will serialize, but correctly
            # but using the actual Hint data type here will cause Multiesrver to crash
            slot_data["hints"] = []
            i = 0
            for hint in self.hints:
                slot_data["hints"].append({})
                slot_data["hints"][i]["id"] = hint.id
                slot_data["hints"][i]["text"] = hint.text
                slot_data["hints"][i]["ignore_other_text"] = hint.ignore_other_text
                i += 1

        return slot_data
