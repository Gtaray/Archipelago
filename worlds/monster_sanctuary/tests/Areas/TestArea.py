import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState, ItemClassification
from worlds import AutoWorld


class TestArea(unittest.TestCase):
    def setUp(self):
        # Copied from ALttP tests
        self.multiworld = MultiWorld(1)
        self.multiworld.game = {1: "Monster Sanctuary"}
        self.multiworld.set_seed(None)

        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types["Monster Sanctuary"].option_definitions.items():
            setattr(args, name, {1: option.from_any(option.default)})

        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()

        self.starting_regions = []  # Where to start exploring
        self.remove_exits = []

        self.multiworld.worlds[1].generate_early()
        self.multiworld.worlds[1].create_regions()

        self.multiworld.get_region('Menu', 1).exits = []
        self.multiworld.worlds[1].create_items()

    def run_tests(self, access_pool):
        for region_exit in self.remove_exits:
            self.multiworld.get_entrance(region_exit, 1).connected_region = self.multiworld.get_region('Menu', 1)

        for location, access, *item_pool in access_pool:
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None

            with self.subTest(location=location, access=access, items=items, all_except=all_except):
                if all_except and len(all_except) > 0:
                    pass
                    # Probably won't need this function
                    # items = self.multiworld.itempool[:]
                    # items = [item for item in items if item.name not in all_except]
                    # items.extend(ItemFactory(item_pool[0], 1))
                else:
                    for i in range(len(items)):
                        items[i] = self.multiworld.create_item(items[i], 1)

                state = CollectionState(self.multiworld)
                state.reachable_regions[1].add(
                    self.multiworld.get_region('Menu', 1)
                )

                for region_name in self.starting_regions:
                    region = self.multiworld.get_region(region_name, 1)
                    state.reachable_regions[1].add(region)
                    for region_exit in region.exits:
                        if region_exit.connected_region is not None:
                            state.blocked_connections[1].add(region_exit)

                for item in items:
                    item.classification = ItemClassification.progression
                    # Don't want to use state.collect() because that sweeps for all other checks
                    # that follows, and we don't want to do that. We only want to use the items we
                    # define the test to use
                    state.prog_items[item.name, 1] += 1

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access)
