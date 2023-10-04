from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class BlobBurgTests(TestArea):
    def test_progression(self):
        self.starting_regions = ["BlobBurg_East1"]
        self.run_tests([
            ["blob_burg_access_1", True, []],

            ["blob_burg_access_2", False, ["Double Jump Boots", "Silvaero"]],
            ["blob_burg_access_2", True, ["Blob Burg Access", "Double Jump Boots", "Silvaero"]],

            ["blob_burg_access_3", False, ["Blob Burg Access", "Double Jump Boots", "Silvaero"]],
            ["blob_burg_access_3", True, ["Blob Burg Access", "Blob Burg Access", "Double Jump Boots",
                                          "Silvaero"]],

            ["blob_burg_access_4", False, ["Blob Burg Access", "Blob Burg Access", "Double Jump Boots",
                                           "Silvaero"]],
            ["blob_burg_access_4", True, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                          "Double Jump Boots", "Silvaero"]],

            ["blob_burg_access_5", False, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                           "Double Jump Boots", "Silvaero", "Koi"]],
            ["blob_burg_access_5", True, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                          "Blob Burg Access", "Double Jump Boots", "Silvaero", "Koi"]],

            ["blob_burg_access_6", False, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                           "Blob Burg Access", "Double Jump Boots", "Silvaero"]],
            ["blob_burg_access_6", True, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                          "Blob Burg Access", "Blob Burg Access", "Double Jump Boots",
                                          "Silvaero"]],

            ["BlobBurg_Worms_3", False, ["Blob Burg Access", "Double Jump Boots", "Silvaero"]],
            ["BlobBurg_Worms_3", True, ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                        "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                        "Double Jump Boots", "Silvaero"]],
        ])
