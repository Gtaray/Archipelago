from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizer import TestMonsterRandomizerBase


class TestFamiliarWolf(TestMonsterRandomizerBase):
    options = {
        "starting_familiar": 0
    }

    def test_starting_familiar(self):
        location = self.multiworld.get_location("Menu_0_1", self.player)
        if self.world.options.starting_familiar == "wolf":
            self.assertEqual(location.item.name, "Spectral Wolf")
        elif self.world.options.starting_familiar == "eagle":
            self.assertEqual(location.item.name, "Spectral Eagle")
        elif self.world.options.starting_familiar == "toad":
            self.assertEqual(location.item.name, "Spectral Toad")
        elif self.world.options.starting_familiar == "lion":
            self.assertEqual(location.item.name, "Spectral Lion")


class TestFamiliarWolf_Shuffle(TestFamiliarWolf):
    options = {
        "starting_familiar": 0,
        "randomize_monsters": 2
    }


class TestSpectralEagle(TestFamiliarWolf):
    options = {
        "starting_familiar": 1
    }


class TestSpectralEagle_Shuffle(TestFamiliarWolf):
    options = {
        "starting_familiar": 1,
        "randomize_monsters": 2
    }


class TestSpectralToad(TestFamiliarWolf):
    options = {
        "starting_familiar": 2
    }


class TestSpectralToad_Shuffle(TestFamiliarWolf):
    options = {
        "starting_familiar": 2,
        "randomize_monsters": 2
    }


class TestSpectralLion(TestFamiliarWolf):
    options = {
        "starting_familiar": 3
    }


class TestSpectralLion_Shuffle(TestFamiliarWolf):
    options = {
        "starting_familiar": 3,
        "randomize_monsters": 2
    }
