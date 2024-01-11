from worlds.monster_sanctuary.tests.Areas.TestArea import TestArea


class BlobBurgTests(TestArea):
    def test_access_1(self):
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_1", [])

    def test_access_2(self):
        self.assertNotAccessible("BlobBurg_East1", "blob_burg_access_2",
                                 ["Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_2",
                              ["Blob Burg Access", "Double Jump Boots", "Kongamato"])

    def test_access_3(self):
        self.assertNotAccessible("BlobBurg_East1", "blob_burg_access_3",
                                 ["Blob Burg Access", "Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_3",
                              ["Blob Burg Access", "Blob Burg Access", "Double Jump Boots", "Kongamato"])

    def test_access_4(self):
        self.assertNotAccessible("BlobBurg_East1", "blob_burg_access_4",
                                 ["Blob Burg Access", "Blob Burg Access", "Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_4",
                              ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                               "Double Jump Boots", "Kongamato"])

    def test_access_5(self):
        self.assertNotAccessible("BlobBurg_East1", "blob_burg_access_5",
                                 ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                  "Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_5",
                              ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                               "Double Jump Boots", "Kongamato", "Koi"])

    def test_access_6(self):
        self.assertNotAccessible("BlobBurg_East1", "blob_burg_access_6",
                                 ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                  "Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "blob_burg_access_6",
                              ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                               "Blob Burg Access", "Double Jump Boots", "Kongamato"])

    def test_access_7(self):
        self.assertNotAccessible("BlobBurg_East1", "BlobBurg_Worms_3",
                                 ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                                  "Blob Burg Access", "Double Jump Boots", "Kongamato"])
        self.assertAccessible("BlobBurg_East1", "BlobBurg_Worms_3",
                              ["Blob Burg Access", "Blob Burg Access", "Blob Burg Access", "Blob Burg Access",
                               "Blob Burg Access", "Blob Burg Access", "Double Jump Boots", "Kongamato"])
