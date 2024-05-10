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

            # if the goal is to defeat the mad lord, then we do not add any post-game locations
            if self.options.goal == "defeat_mad_lord" and location_data.name in LOCATIONS.postgame_locations:
                continue

            # if the goal is to defeat the mad lord or defeat all champions, then we do not add any
            # locations that require a rank of keeper master
            if ((self.options.goal == "defeat_mad_lord" or self.options.goal == "defeat_all_champions")
                    and location_data.name in LOCATIONS.keeper_master_locations):
                continue

            # If the goal is to reunite mozzie, then we don't include velvet melody locations in the pool
            if self.options.goal == "reunite_mozzie" and location_data.name in LOCATIONS.velvet_melody_locations:
                continue

            # If the underworld starts opened, then don't add the item checks for the Eric fight
            if (self.options.open_underworld
                    and location_data.name in ["Blue Cave - Underworld Entrance 1", "Blue Cave - Underworld Entrance 2"]):
                continue

            # Unless eggsanity is enabled, don't add eggsanity locations
            if not self.options.eggsanity and location_data.category == MonsterSanctuaryLocationCategory.EGGSANITY:
                continue

            # Unless monster army is enabled, do not add monster army locations
            if not self.options.monster_army and location_data.category == MonsterSanctuaryLocationCategory.ARMY:
                continue

            # Unless shopsanity is enabled, do not add shop locations
            if not self.options.shopsanity and location_data.category == MonsterSanctuaryLocationCategory.SHOP:
                continue

            # If the shop check requires keeper rank 9, and shops_ignore_rank is not enabled,
            # and the goal doesn't allow for keeper rank 9, then we skip this location
            if (self.options.shopsanity
                    and not self.options.shops_ignore_rank
                    and location_data.name in LOCATIONS.shopsanity_keeper_master_locations
                    and (self.options.goal == "defeat_mad_lord" or self.options.goal == "defeat_all_champions")):
                continue

            # First we check if we should be ignoring these locations based on rando options
            # If we're never allowing shifting, then these locations should not be included, as they
            # require a shifted monster to get.
            if self.options.monster_shift_rule == "never" and location_data.name in [
                "Snowy Peaks - Cryomancer - Light Egg Reward",
                "Snowy Peaks - Cryomancer - Dark Egg Reward"
            ]:
                continue

            # Do not add a location for the player's own familiar in eternity's end
            if (self.options.starting_familiar == "wolf"
                    and location_data.name in LOCATIONS.eternitys_end_locations["wolf"]):
                continue
            if (self.options.starting_familiar == "eagle"
                    and location_data.name in LOCATIONS.eternitys_end_locations["eagle"]):
                continue
            if (self.options.starting_familiar == "toad"
                    and location_data.name in LOCATIONS.eternitys_end_locations["toad"]):
                continue
            if (self.options.starting_familiar == "lion"
                    and location_data.name in LOCATIONS.eternitys_end_locations["lion"]):
                continue

            region = self.multiworld.get_region(location_data.region, self.player)
            access_condition = location_data.access_condition or None

            # Here we check if shops should ignore rank requirements
            # We have to call out this specifically in order to null out the access_condition
            if location_data.category == MonsterSanctuaryLocationCategory.SHOP and self.options.shops_ignore_rank:
                access_condition = None

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

            # Chest, Gift, Monster Army, and Shop locations go here
            else:
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

                access_condition = connection.access_rules or None

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

        elif self.options.goal == "complete_monster_journal":
            self.multiworld.completion_condition[self.player] = lambda state: (
                RULES.has_all_monsters(state, self.player)
            )

        elif self.options.goal == "reunite_mozzie":
            self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Mozzie", self.player, self.options.mozzie_soul_fragments)
                and RULES.velvet_melody_access(state, self.player)
                # This requirement is only here as an artificial gate for having a
                # high enough level team to defeat Velvet Melody
                and RULES.keeper_rank_6(state, self.player)
            )

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
            # If blob burg is unlocked, we don't need to place the blob key used events
            if (location_name in ["stronghold_dungeon_blob_key", "mystical_workshop_blob_key", "sun_palace_blob_key"]
                    and (self.options.open_blob_burg == "entrances" or self.options.open_blob_burg == "full")):
                continue

            # If magma chamber is open, don't place the flag to lower the lava
            if (location_name == "magma_chamber_lower_lava" and
                    (self.options.open_magma_chamber == "lower_lava" or self.options.open_magma_chamber == "full")):
                continue

            region = self.multiworld.get_region(data.region, self.player)
            access_condition = data.access_condition or None
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

        # Start with spectral familiars,
        # these aren't currently shuffled at all, so they don't need to go in the conditional blocks
        if self.options.starting_familiar == "wolf":
            eggs["Eternity's End - Spectral Familiar Egg (Eagle)"] = self.create_item("Spectral Eagle Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Toad)"] = self.create_item("Spectral Toad Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Lion)"] = self.create_item("Spectral Lion Egg")
        elif self.options.starting_familiar == "eagle":
            eggs["Eternity's End - Spectral Familiar Egg (Wolf)"] = self.create_item("Spectral Wolf Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Toad)"] = self.create_item("Spectral Toad Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Lion)"] = self.create_item("Spectral Lion Egg")
        elif self.options.starting_familiar == "toad":
            eggs["Eternity's End - Spectral Familiar Egg (Wolf)"] = self.create_item("Spectral Wolf Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Eagle)"] = self.create_item("Spectral Eagle Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Lion)"] = self.create_item("Spectral Lion Egg")
        elif self.options.starting_familiar == "lion":
            eggs["Eternity's End - Spectral Familiar Egg (Wolf)"] = self.create_item("Spectral Wolf Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Eagle)"] = self.create_item("Spectral Eagle Egg")
            eggs["Eternity's End - Spectral Familiar Egg (Toad)"] = self.create_item("Spectral Toad Egg")

        if self.options.randomize_monsters == "by_specie":
            # These eggs either get added to the item pool or they are placed in their respective gift location
            eggs["Sun Palace - Caretaker 1"] = self.create_item(self.species_swap["Koi"].egg_name())
            # We never actually species swap Bard, so this is a bit redundant, but having it here makes it
            # clear that it should be handled here even if we did swap it
            eggs["Forgotten World - Wanderer Room"] = self.create_item(self.species_swap["Bard"].egg_name())
            eggs["Magma Chamber - Bex"] = self.create_item(self.species_swap["Skorch"].egg_name())
            eggs["Snowy Peaks - Cryomancer - Egg Reward 1"] = self.create_item(self.species_swap["Shockhopper"].egg_name())
            eggs["Snowy Peaks - Cryomancer - Light Egg Reward"] = self.create_item(self.species_swap["Shockhopper"].egg_name())
            eggs["Snowy Peaks - Cryomancer - Dark Egg Reward"] = self.create_item(self.species_swap["Shockhopper"].egg_name())

            # These are straight up added because they don't come from a specific location
            # they just need to be available in the pool somewhere to make sure all monsters
            # are available.
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
            eggs["Snowy Peaks - Cryomancer - Egg Reward 1"] = self.create_item("Shockhopper Egg")
            eggs["Snowy Peaks - Cryomancer - Light Egg Reward"] = self.create_item("Shockhopper Egg")
            eggs["Snowy Peaks - Cryomancer - Dark Egg Reward"] = self.create_item("Shockhopper Egg")

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

        self.handle_relics(pool, item_exclusions)
        self.handle_key_items(pool)
        self.handle_explore_ability_items(pool)

        while len(pool) < self.number_of_item_locations:
            item_name = ITEMS.get_random_item_name(self, pool, group_exclude=item_exclusions)
            if item_name is not None:
                pool.append(self.create_item(item_name))

        self.multiworld.itempool += pool

    def handle_relics(self, pool: List[MonsterSanctuaryItem], item_exclusions: List[str]):
        # Exclude relics of chaos if the option isn't enabled
        relics: List[ItemData] = []
        if self.options.include_chaos_relics == "off":
            item_exclusions.append("Relic")
        elif self.options.include_chaos_relics == "on":
            pass  # Relics can be randomly put in the item pool, nothing to do here.
        elif self.options.include_chaos_relics == "some":
            relics = self.random.sample(ITEMS.get_items_in_group("Relic"), 5)
        elif self.options.include_chaos_relics == "all":
            relics = ITEMS.get_items_in_group("Relic")

        for relic in relics:
            relic_name = ITEMS.roll_random_equipment_level(self, relic)
            pool.append(self.create_item(relic_name))

    def handle_key_items(self, pool: List[MonsterSanctuaryItem]):
        key_items = [item_name for item_name in ITEMS.item_data
                     if ITEMS.item_data[item_name].category == MonsterSanctuaryItemCategory.KEYITEM]

        # If blob burg is unlocked via options, then remove the blob key from the item pool
        if self.options.open_blob_burg == "entrances" or self.options.open_blob_burg == "full":
            key_items.remove("Blob Key")

        # If magma chamber has its lava lowered via options, remove runestone shard from the item pool
        if self.options.open_magma_chamber == "lower_lava" or self.options.open_magma_chamber == "full":
            key_items.remove("Runestone Shard")

        if self.options.open_abandoned_tower == "entrances" or self.options.open_abandoned_tower == "full":
            key_items.remove("Key of Power")

        # If the underworld entrance is opened up, don't add sanctuary tokens to the item pool
        if self.options.open_underworld == "entrances" or self.options.open_underworld == "full":
            key_items = [i for i in key_items if i != "Sanctuary Token"]

        # Add items that are not technically key items, but are progressions items and should be added
        key_items.append("Raw Hide")
        key_items.extend([name for name, item in ITEMS.item_data.items()
                          if item.category == MonsterSanctuaryItemCategory.CATALYST])

        if self.options.goal == "reunite_mozzie":
            # -1 because one mozzie is added from key items list
            for i in range(self.options.mozzie_soul_fragments.value - 1):
                key_items.append("Mozzie")

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

    def handle_explore_ability_items(self, pool: List[MonsterSanctuaryItem]):
        explore_items = ITEMS.get_explore_ability_items(self.options.lock_explore_abilities.value)

        for item in explore_items:
            pool.append(self.create_item(item.name))

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

        # Combat traps should only be placed in other players' worlds.
        self.options.non_local_items.value |= self.item_name_groups["Combat Trap"]

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    def generate_basic(self) -> None:
        self.set_victory_condition()
        self.place_ranks()

    # creates the output files if there is output to be generated. When this is called,
    # self.multiworld.get_locations(self.player) has all locations for the player, with attribute
    # item pointing to the item. location.item.player can be used to see if it's a local item.
    def generate_output(self, output_directory: str) -> None:
        pass
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player),
        #                   "D:\\Visual Studio Projects\\Archipelago\\worlds\\monster_sanctuary\\world.puml")

    def generate_shopsanity_prices(self):
        min_price = 10
        max_price = 5000

        self.shopsanity_prices: Dict[int, int] = {}
        shop_locations = LOCATIONS.get_locations_of_type(MonsterSanctuaryLocationCategory.SHOP)

        for location_data in shop_locations:
            location = self.multiworld.get_location(location_data.name, self.player)
            if location is None:
                continue

            weight = (min_price + max_price) / 2
            if self.options.shopsanity_prices == "weighted":
                if location.item.classification == ItemClassification.progression:
                    weight = weight + (weight/2)
                elif location.item.classification == ItemClassification.filler:
                    weight = weight / 4

            self.shopsanity_prices[location.address] = round(self.random.triangular(min_price, max_price, weight))

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self) -> dict:
        if self.options.hints:
            self.hint_rng = self.random
            HINTS.generate_hints(self)

        if self.options.shopsanity and self.options.shopsanity_prices != "normal":
            self.generate_shopsanity_prices()

        slot_data = {
            "version": "1.1.4"
        }

        # Rando options
        slot_data["options"] = {
            "goal": self.options.goal.value,
            "death_link": self.options.death_link.value,
            "remove_locked_doors": self.options.remove_locked_doors.value,
            "skip_plot": self.options.skip_plot.value,
            "open_blue_caves": self.options.open_blue_caves.value,
            "open_stronghold_dungeon": self.options.open_stronghold_dungeon.value,
            "open_ancient_woods": self.options.open_ancient_woods.value,
            "open_snowy_peaks": self.options.open_snowy_peaks.value,
            "open_sun_palace": self.options.open_sun_palace.value,
            "open_horizon_beach": self.options.open_horizon_beach.value,
            "open_magma_chamber": self.options.open_magma_chamber.value,
            "open_forgotten_world": self.options.open_forgotten_world.value,
            "open_blob_burg": self.options.open_blob_burg.value,
            "open_underworld": self.options.open_underworld.value,
            "open_mystical_workshop": self.options.open_mystical_workshop.value,
            "open_abandoned_tower": self.options.open_abandoned_tower.value,
            "eggsanity": self.options.eggsanity.value,
            "monster_army": self.options.monster_army.value,
            "starting_familiar": self.options.starting_familiar.value,
            "exp_multiplier": self.options.exp_multiplier.value,
            "monsters_always_drop_egg": self.options.monsters_always_drop_egg.value,
            "monster_shift_rule": self.options.monster_shift_rule.value,
            "add_smoke_bombs": self.options.add_smoke_bombs.value,
            "starting_gold": self.options.starting_gold.value,
            "shops_ignore_rank": self.options.shops_ignore_rank.value,
            "lock_explore_abilities": self.options.lock_explore_abilities.value,
            "include_chaos_relics": self.options.include_chaos_relics.value,
        }

        if self.options.goal == "reunite_mozzie":
            slot_data["options"]["mozzie_pieces"] = self.options.mozzie_soul_fragments.value

        tanuki_location = self.multiworld.get_location("Menu_1_0", self.player)
        slot_data["monsters"] = {
            "tanuki": tanuki_location.item.name,
        }

        # If we're shuffling monsters, we want the client to know what we shuffled to
        if self.options.randomize_monsters == "by_specie":
            slot_data["monsters"]["bex_monster"] = self.species_swap["Skorch"].name
            # slot_data["monsters"]["species_swap"] = {}
            # for original_monster, new_monster in self.species_swap.items():
            #     slot_data["monsters"]["species_swap"][original_monster] = new_monster.name

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
                if len(encounter.monsters) > 1:
                    monster = encounter.monsters[1]

                # We only need the scene name to be able to map champions
                slot_data["monsters"]["champions"][f"{parts[0]}_{parts[1]}"] = monster.name

        slot_data["locations"] = {}
        slot_data["locations"]["ranks"] = {}
        for location in self.multiworld.get_locations(self.player):
            region = location.parent_region
            if '_' in location.name:  # Ignore monster locations and flags
                continue
            if location.item.code is None:  # Ignore events
                continue

            # With shopsanity enabled, shop locations go in their own special bucket
            # and aren't counted as the normal amount of checks for a region
            if self.options.shopsanity and LOCATIONS.is_location_shop(location.logical_name):
                if "shops" not in slot_data["locations"]:
                    slot_data["locations"]["shops"] = {}
                slot_data["locations"]["shops"][location.name] = location.address

                if self.options.shopsanity_prices != "normal":
                    if "prices" not in slot_data:
                        slot_data["prices"] = {}
                    slot_data["prices"][location.name] = self.shopsanity_prices[location.address]
                continue

            name = LOCATIONS.get_location_name_for_client(location.logical_name)
            if name is None:
                continue

            area = region.name.split("_")[0]
            if area not in slot_data["locations"]:
                slot_data["locations"][area] = {}

            slot_data["locations"][area][name] = location.address

            # If this is a champion defeated item, then add it to the ranks dictionary
            if location.logical_name.endswith("_Champion"):
                slot_data["locations"]["ranks"][name] = location.address

        if self.options.hints and hasattr(self, "hints"):
            # There's probably a much better way of doing this.
            # I just want an anonymous object that will serialize correctly
            # but using the actual Hint data type here will cause Multiserver to crash
            slot_data["hints"] = []
            i = 0
            for hint in self.hints:
                slot_data["hints"].append({})
                slot_data["hints"][i]["id"] = hint.id
                slot_data["hints"][i]["text"] = hint.text
                slot_data["hints"][i]["ignore_other_text"] = hint.ignore_other_text
                i += 1

        return slot_data
