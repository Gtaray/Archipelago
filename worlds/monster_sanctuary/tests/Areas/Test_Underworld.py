from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class UnderworldTests(TestArea):
    def test_shortcuts(self):
        self.starting_regions = ["Underworld_EastCatacomb6_East"]
        self.run_tests([
            ["underworld_east_catacomb_6_shortcut", False, []],
            ["underworld_east_catacomb_6_shortcut", True, ["Underworld East Catacomb 6 Shortcut"]]
        ])

        self.starting_regions = ["Underworld_EastCatacomb3"]
        self.run_tests([
            ["underworld_east_catacomb_pillar_control", False, []],
            ["underworld_east_catacomb_pillar_control", True, ["Underworld East Catacomb 8 Shortcut"]]
        ])

        self.starting_regions = ["Underworld_WestCatacomb4_Upper"]
        self.run_tests([
            ["Underworld_WestCatacomb4_Lower_11", False, []],
            ["Underworld_WestCatacomb4_Lower_11", True, ["Underworld West Catacomb 4 Shortcut"]]
        ])

        self.starting_regions = ["Underworld_WestCatacomb7_Shortcut"]
        self.run_tests([
            ["underworld_west_catacomb_7_shortcut", False, []],
            ["underworld_west_catacomb_7_shortcut", True, ["Underworld West Catacomb 7 Shortcut"]],
        ])

    def test_keys(self):
        self.starting_regions = ["Underworld_EastCatacomb3"]
        self.run_tests([
            ["underworld_east_catacomb_7_access", False, []],
            ["underworld_east_catacomb_unlocked", True, ["Underworld key"]],
            ["underworld_east_catacomb_unlocked", False, ["Underworld key", "Underworld Key Used"]],
            ["underworld_east_catacomb_7_access", True, ["Underworld East Catacomb Unlocked"]]
        ])

    def test_progression(self):
        # East catacomb progression
        self.starting_regions = ["Underworld_Entrance"]
        self.run_tests([
            # First check that we can't access the end right away
            ["underworld_east_catacomb_pillar_control", False, []],
            ["Underworld_Center1_29000021", False, []],
            # Then we check if we can get the key, which is the first logical part of this
            ["underworld_east_catacomb_unlocked", False, []],
            ["Underworld_EastCatacomb6_East_4", True, []],
            # After getting the key, check that we have access to this room
            ["underworld_east_catacomb_unlocked", True, ["Underworld key"]],
            ["underworld_east_catacomb_7_access", True, ["Underworld East Catacomb Unlocked"]],
            # Once catacomb 7 is accessible, test that we can go to the controls, and then progress past
            ["underworld_east_catacomb_pillar_control", True, ["Underworld East Catacomb 7 Access"]],
            ["Underworld_Center1_29000021", True, ["Underworld East Catacomb Pillar Control"]],
        ])

        # West catacomb progression
        self.starting_regions = ["Underworld_Center2"]
        self.run_tests([
            # Test that we can't get to the end right away
            ["Underworld_WestCatacomb9_Interior_Champion", False, []],
            ["Underworld_WestCatacomb1_8", False, []],

            # First check that we can get in to the catacomb from both directions
            ["Underworld_WestCatacomb1_8", True, ["Double Jump Boots", "Kongamato"]],
            ["underworld_west_catacomb_center_entrance", True, ["Double Jump Boots", "Kongamato"]],
            ["underworld_west_catacomb_4_shortcut", False, []],
            ["underworld_west_catacomb_4_shortcut", True, ["Underworld West Catacomb Center Entrance", "Vaero"]],

            # Once inside, you need to access the west half of catacomb 4 through catacomb 3
            ["underworld_west_catacomb_4_access", False, []],
            ["underworld_west_catacomb_4_access", True, ["Double Jump Boots", "Kongamato", "Brutus"]],
            ["underworld_west_catacomb_4_access", True, ["Double Jump Boots", "Kongamato", "Underworld West Catacomb 4 Access"]],

            # Now get access to the catacomb 7 shortcut
            # There might be another requirement to get to this location, but that will require player experience
            ["underworld_west_catacomb_7_shortcut", False, []],
            ["underworld_west_catacomb_7_shortcut", True, ["Double Jump Boots", "Kongamato"]],

            # Now the player needs roof access so they can do the final loop around the building
            # There might be another requirement to get to this location, but that will require player experience
            ["underworld_west_catacomb_roof_access", False, []],
            ["underworld_west_catacomb_roof_access", True, ["Double Jump Boots", "Kongamato"]],

            # Finally put it all together to get to the end
            ["underworld_west_catacomb_9_interior_access", True, [
                "Double Jump Boots", "Kongamato",
                "Underworld West Catacomb Center Entrance",
                "Underworld West Catacomb 4 Shortcut",
                "Underworld West Catacomb 4 Access",
                "Underworld West Catacomb 7 Shortcut",
                "Underworld West Catacomb Roof Access",
            ]]
        ])
