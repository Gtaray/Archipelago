from typing import List, Set, Dict

from BaseClasses import Item, MultiWorld, Tutorial, Location, ItemClassification
from Options import Range, Toggle, VerifyKeys
from worlds.AutoWorld import World, WebWorld

from .items import item_table, MonsterSanctuaryItem
from .items import MonsterSanctuaryItemCategory as ItemCategory
from .locations import location_table
from .locations import MonsterSanctuaryLocationCategory as LocationCategory
from .regions import create_regions
from .rules import set_rules
from .options import monster_sanctuary_options


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


class MonsterSanctuaryWorld(World):
    game = "Monster Sanctuary"
    web = MonsterSanctuaryWebWorld()
    option_definitions = monster_sanctuary_options

    data_version = 0

    topology_present = True

    items.build_item_ids()
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    item_name_groups = items.build_item_groups()

    locations.build_location_ids()
    location_name_to_id = {location.name: location.id for location in location_table
                           if location.id is not None}

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

    # called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate,
    # this can be done during generate_early or create_items as well.
    def create_regions(self) -> None:
        # This not only creates all the regions within the world
        # but assigns all locations to their respective regions
        create_regions(self.multiworld, self.player)

        # Place monsters
        print("Placing Monsters")
        # Globally Maps one mon to another mon. This is only used if option randomize_monsters is by specie
        monster_map = {}
        champion_map = locations.get_shuffled_champion_map(self)

        for region in self.multiworld.regions:
            for location in region.locations:
                # We're only handling monster, champion, and keeper locations here
                if not (location.category == LocationCategory.MONSTER
                        or location.category == LocationCategory.CHAMPION
                        or location.category == LocationCategory.KEEPER
                        or location.category == LocationCategory.RANK):
                    continue

                monster_name: str

                if location.category == LocationCategory.RANK:
                    location.place_locked_item(self.create_item("Champion Defeated"))
                    continue

                # TODO: Add a global list to pull from so that mons don't get re-used til all monsters have been placed
                if (location.category == LocationCategory.MONSTER or
                    (location.category == LocationCategory.CHAMPION and self.randomize_champions == "default")):
                    if self.randomize_monsters == "no":
                        monster_name = location.default_item;

                    # if randomizing by specie, we map all monsters 1 to 1 with another monster
                    elif self.randomize_monsters == "by_specie":
                        if monster_map.get(location.default_item) is None:
                            monster_map[location.default_item] = items.get_random_monster_name(self)
                        monster_name = monster_map[location.default_item]

                    # if randomizing by encounter, every encounter maps monsters 1 to 1 with another monster
                    elif self.randomize_monsters == "by_encounter":
                        if monster_map.get(location.name) is None:
                            monster_map[location.name] = {}
                        if monster_map[location.name].get(location.default_item) is None:
                            monster_map[location.name][location.default_item] = items.get_random_monster_name(self)
                        monster_name = monster_map[location.name][location.default_item]

                    else:
                        monster_name = items.get_random_monster_name(self)

                elif location.category == LocationCategory.CHAMPION:
                    if self.randomize_champions == "no":
                        monster_name = location.default_item

                    # We should never hit this, becuse the default case it handled above with the MONSTER type
                    elif self.randomize_champions == "default":
                        pass

                    elif self.randomize_champions == "shuffle":
                        monster_name = champion_map[location.default_item]

                    # TODO: Probably add more detail to this?
                    elif self.randomize_champions == "random":
                        monster_name = items.get_random_monster_name(self)

                # TODO: Add option to not randomize keepers, or to use generic monster pool settings
                elif location.category == LocationCategory.KEEPER:
                    monster_name = items.get_random_monster_name(self)

                # create the item
                monster = self.create_item(monster_name)

                # Monsters placed in keeper battles need to be marked as NOT progression
                if location.category == LocationCategory.KEEPER:
                    monster.classification = ItemClassification.filler

                # Place the selected monster
                location.place_locked_item(monster)

                print(f"{location.name}: {location.default_item} -> {monster_name}")

    # called to place player's items into the MultiWorld's itempool. After this step all regions and items have to
    # be in the MultiWorld's regions and itempool, and these lists should not be modified afterward.
    def create_items(self) -> None:
        # Just get this working
        # Add the only key item required for the first area
        pool: list[MonsterSanctuaryItem] = []

        # These items are not naturally put in the general item pool, and are handled separately
        item_exclusions = ["Multiple"]

        # Exclude relics of chaos if the option isn't enabled
        if not self.include_chaos_relics:
            item_exclusions.append("Relic")

        for location in location_table:
            # Monsters and champions are placed in create_regions
            if (location.category == LocationCategory.MONSTER
                    or location.category == LocationCategory.CHAMPION
                    or location.category == LocationCategory.KEEPER):
                continue

            # If this location contains a key item, add it and move on.
            # This should handle key items that show up multiple times
            if items.is_item_type(location.default_item, ItemCategory.KEYITEM):
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

            # For debugging purposes.
            print(location.default_item + " -> " + item_name)

        self.multiworld.itempool += pool

    # create any item on demand
    def create_item(self, item: str) -> MonsterSanctuaryItem:
        return MonsterSanctuaryItem(item, items.item_table[item], self.player)

    # called to set access and item rules on locations and entrances. Locations have to be defined before this,
    # or rule application can miss them.
    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    # called after the previous steps. Some placement and player specific randomizations can be done here.
    # def generate_basic(self) -> None:
    #     pass

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

    # fill_slot_data and modify_multidata can be used to modify the data that will be used by
    # the server to host the MultiWorld.
    def fill_slot_data(self):
        pass
