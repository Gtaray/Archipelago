import copy
from enum import IntEnum
from random import Random
from typing import Dict, List, Optional

from .rules import AccessCondition
from BaseClasses import MultiWorld
from ..AutoWorld import World


class GameStage(IntEnum):
    EARLY = 0
    LATE = 1


class MonsterData:
    id: int
    name: str
    groups: List[str]
    stage: Optional[GameStage] = None
    pre_evolution: Optional[str] = None

    def __init__(self, id: int, name: str, groups: List[str]):
        # This needs to exist alongside normal item ids, because monsters will ultimately be classified as items
        # Because event locations need to hold items with ids
        self.id = id
        self.name = name
        self.groups = groups

        if self.name in evolved_monsters:
            self.pre_evolution = evolved_monsters[self.name]

    def __str__(self):
        return self.name

    def is_evolved(self):
        return self.name in evolved_monsters

    def is_pre_evolved(self):
        return self.name in list(evolved_monsters.values())

    def egg_name(self):
        if self.name == "Plague Egg":
            return "??? Egg"
        if self.pre_evolution is not None:
            return f"{self.pre_evolution} Egg"
        return f"{self.name} Egg"


class EncounterData:
    encounter_id: int
    name: str
    monsters: List[MonsterData]
    champion: bool = False
    region: str
    area: str
    access_condition = Optional[AccessCondition]
    monster_exclusions: List[str]

    def __init__(self,
                 encounter_id: int,
                 encounter_name: str,
                 is_champion: bool,
                 region: str,
                 access_condition: AccessCondition):
        self.encounter_id = encounter_id
        self.name = encounter_name
        self.champion = is_champion
        self.region = region
        self.area = self.region.split("_")[0]
        self.access_condition = access_condition
        self.monsters = []
        self.monster_exclusions = []

    def __str__(self):
        return f"{self.name}: {', '.join([monster.name for monster in self.monsters])}"

    def add_monster(self, monster: MonsterData):
        self.monsters.append(monster)

    def add_exclusion(self, *monsters: str):
        for monster in monsters:
            if monster not in self.monster_exclusions:
                self.monster_exclusions.append(monster)

    def replace_monsters(self, *new_monsters: MonsterData):
        if len(new_monsters) != len(self.monsters):
            raise ValueError(
                f"Could not replace monsters for encounter {self.name}. Number of monsters does not match.")

        self.monsters = list(new_monsters)


monster_data: Dict[str, MonsterData] = {}
encounter_data: Dict[str, EncounterData] = {}

evolved_monsters = {
    "G'rulu": "Grummy",
    "Magmamoth": "Magmapillar",
    "Megataur": "Minitaur",
    "Ninki Nanka": "Ninki",
    "Sizzle Knight": "Crackle Knight",
    "Silvaero": "Vaero",
    "Glowdra": "Glowfly",
    "Dracogran": "Draconov",
    "Dracozul": "Draconov",
    "Mega Rock": "Rocky",
    "Draconoir": "Draconov",
    "King Blob": "Blob",
    "Mad Lord": "Mad Eye",
    "Ascendant": "Monk",
    "Fumagus": "Fungi",
    "Dracomer": "Draconov"
}
early_game_areas: List[str] = ["Menu", "MountainPath", "BlueCave", "KeepersStronghold", "KeepersTower",
                               "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods"]
late_game_areas: List[str] = ["HorizonBeach", "MagmaChamber", "BlobBurg", "ForgottenWorld", "MysticalWorkshop",
                              "Underworld", "AbandonedTower", "EternitysEnd"]


# region Data Loading
def add_encounter(encounter: EncounterData, monsters: List[str]) -> None:
    if encounter_data.get(encounter.name) is not None:
        raise KeyError(f"{encounter.name} already exists in encounters_data")

    for monster_name in monsters:
        encounter.add_monster(get_monster(monster_name))

    encounter_data[encounter.name] = encounter
# endregion


# region Monster and Champion Randomization
# UNUSED
def assign_familiar(world: World) -> None:
    if world.options.spectral_familiar == "wolf":
        world.encounters["Menu_0"].add_monster(get_monster("Spectral Wolf"))
    elif world.options.spectral_familiar == "eagle":
        world.encounters["Menu_0"].add_monster(get_monster("Spectral Eagle"))
    elif world.options.spectral_familiar == "toad":
        world.encounters["Menu_0"].add_monster(get_monster("Spectral Toad"))
    elif world.options.spectral_familiar == "lion":
        world.encounters["Menu_0"].add_monster(get_monster("Spectral Lion"))


def randomize_monsters(world: World) -> None:
    assign_game_stage_to_monsters()
    set_encounter_monster_exclusions(world)

    # This holds the data for all encounter locations used by the world.
    # We store it here so that encounter_data can remain immutable while randomizing
    world.encounters = copy.deepcopy(encounter_data)

    # If we're not randomizing, we can bail out here.
    if world.options.randomize_monsters == "off":
        return

    random = world.random
    encounters_to_randomize = [encounter for name, encounter in world.encounters.items()]
    available_monsters = get_monsters()

    # if shuffling, then we shuffle the species
    # if not shuffling, then we place the required monsters
    if world.options.randomize_monsters == "by_specie":
        shuffle_species(world)

    # Fully randomized and randomized by encounter are both handled here
    else:
        # Start by hard-placing some monsters to ensure that certain abilities show
        def place_ability_in_area(abilities: List[str], areas: List[str]):
            encounters = [encounter for encounter in encounters_to_randomize if encounter.area in areas]
            encounter = random.choice(encounters)
            new_monster = random.choice([mon for mon in available_monsters if set(abilities) & set(mon.groups)])

            replace_monsters_in_encounter(world, encounter, available_monsters, new_monster)
            encounters_to_randomize.remove(encounter)

        place_ability_in_area(["Breakable Walls"], ["MountainPath", "BlueCave"])
        place_ability_in_area(["Flying"], ["MountainPath", "BlueCave"])
        place_ability_in_area(
            ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"],
            ["MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace"])

        place_ability_in_area(["Water Orbs"],
                              ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace",
                               "AncientWoods"])
        place_ability_in_area(["Fire Orbs"],
                              ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace",
                               "AncientWoods"])
        place_ability_in_area(["Lightning Orbs"],
                              ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace",
                               "AncientWoods"])
        place_ability_in_area(["Earth Orbs"],
                              ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace",
                               "AncientWoods"])

    # We've either shuffled the monster dictionary (if set to shuffle)
    # Or placed necessary monsters into areas (if set to a different randomize setting)
    # Now we just go through each encounter left and randomize them.
    for encounter in encounters_to_randomize:
        replace_monsters_in_encounter(world, encounter, available_monsters)

    # Lastly, assign familiars. Do this at the end so it doesn't get randomized.
    # assign_familiar(world)


def assign_game_stage_to_monsters():
    for encounter_name, encounter in encounter_data.items():
        stage: GameStage

        if encounter.area in early_game_areas:
            stage = GameStage.EARLY
        elif encounter.area in late_game_areas:
            stage = GameStage.LATE

        for monster in encounter.monsters:
            if monster.stage is None or stage < monster.stage:
                monster.stage = stage


def set_encounter_monster_exclusions(world: World):
    """Sets up rules for which monsters cannot appear at certain locations"""
    if world.options.goal == "defeat_mad_lord":
        mad_lord = encounter_data["AbandonedTower_Final_1"]
        mad_lord.add_exclusion("Akhlut")
        mad_lord.add_exclusion("Krakaturtle")
        mad_lord.add_exclusion("Gryphonix")
        mad_lord.add_exclusion("Bard")
        mad_lord.add_exclusion("Tar Blob")

        # if the cryomancer locations are in the pool,
        # Dodo can't be on the mad lord slot
        if world.options.monster_shift_rule != "never":
            mad_lord.add_exclusion("Dodo")

    # if there's regions where improved mobility are illegal, set it up.
    if world.options.improved_mobility_limit:
        encounters = [encounter for encounter in encounter_data.values()
                      if encounter.area in early_game_areas]
        monsters = [monster.name for monster in get_monsters_with_abilities(
            "Improved Flying", "Lofty Mount", "Improved Swimming", "Dual Mobility")]
        for encounter in encounters:
            encounter.add_exclusion(*monsters)


def shuffle_species(world: World):
    """Shuffles the monster specie dictionary, adhering to all the relevant monster placement rules"""
    if world.options.randomize_monsters != "by_specie":
        return

    world.species_swap = {}
    random = world.random
    available_monsters = get_monsters()

    # These monsters should never be shuffled
    world.species_swap["Spectral Wolf"] = get_monster("Spectral Wolf")
    world.species_swap["Spectral Toad"] = get_monster("Spectral Toad")
    world.species_swap["Spectral Eagle"] = get_monster("Spectral Eagle")
    world.species_swap["Spectral Lion"] = get_monster("Spectral Lion")
    world.species_swap["Bard"] = get_monster("Bard")

    # Start by placing necessary monsters
    def place_ability_in_area(abilities: List[str], areas: List[str]):
        # Pick a monster that hasn't already been shuffled, and is in the right areas
        # then swap it with a new monster that has the correct ability
        monsters = [mon for mon in get_monsters_in_area(world, *areas) if mon.name not in world.species_swap]
        if len(monsters) == 0:
            breakpoint()
        original_monster = random.choice(monsters)
        new_monster = random.choice([mon for mon in available_monsters
                                     if set(abilities) & set(mon.groups)])

        world.species_swap[original_monster.name] = new_monster
        available_monsters.remove(new_monster)

    place_ability_in_area(["Breakable Walls"], ["MountainPath", "BlueCave"])
    place_ability_in_area(["Flying"], ["MountainPath", "BlueCave"])
    place_ability_in_area(
        ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"],
        ["MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace"])
    place_ability_in_area(["Water Orbs"],
                          ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods"])
    place_ability_in_area(["Fire Orbs"],
                          ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods"])
    place_ability_in_area(["Lightning Orbs"],
                          ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods"])
    place_ability_in_area(["Earth Orbs"],
                          ["MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods"])

    # Then shuffle monsters that have limited options based on exclusions in encounters
    def place_monsters_in_encounter_with_exclusions(encounter: EncounterData):
        for original_monster in encounter.monsters:
            # If we've already swapped this monster, then ignore it and move on
            if original_monster.name in world.species_swap:
                continue

            available = [mon for mon in available_monsters if mon.name not in encounter.monster_exclusions]
            new_monster = random.choice(available)
            world.species_swap[original_monster.name] = new_monster
            available_monsters.remove(new_monster)

    for name, enc in world.encounters.items():
        if len(enc.monster_exclusions) > 0:  # Ignore encounters with no exclusions
            place_monsters_in_encounter_with_exclusions(enc)

    # Shuffle the remainder of available monsters
    keys = [monster.name for monster in get_monsters() if monster.name not in world.species_swap]
    values = available_monsters
    random.shuffle(values)
    for i in range(len(keys)):
        world.species_swap[keys[i]] = values[i]

    if len(world.species_swap) != len(monster_data):
        for monster in [name for name in monster_data if name not in world.species_swap]:
            print(f"WARNING: {monster} was not swapped")


def replace_monsters_in_encounter(world: World, encounter: EncounterData, available_monsters: List[MonsterData],
                                  forced_monster: Optional[MonsterData] = None):
    random = world.random
    new_monsters = []

    if world.options.randomize_monsters == "any":
        # Fill out the rest of the monster slots with random monsters
        if forced_monster is not None:
            new_monsters.append(forced_monster)
            available_monsters.remove(forced_monster)

        while len(new_monsters) < len(encounter.monsters):
            picks = [monster for monster in available_monsters if monster.name not in encounter.monster_exclusions]

            # If we're out of monsters to pick from, then reset the list
            if len(picks) == 0:
                available_monsters = get_monsters()
                picks = [monster for monster in available_monsters if monster.name not in encounter.monster_exclusions]

            mon = random.choice(picks)
            new_monsters.append(mon)
            available_monsters.remove(mon)

        # Finally, shuffle the monsters for good measure
        world.random.shuffle(new_monsters)

    elif world.options.randomize_monsters == "by_specie":
        # We've already shuffled species around, so all we do is build the list of new monsters based on that.
        for monster in encounter.monsters:
            new_monsters.append(world.species_swap[monster.name])

    elif world.options.randomize_monsters == "by_encounter":
        # Get a dictionary of monsters in the encounter indexed by their name. If a monster shows up multiple
        # times, it only gets one entry. This enables us to swap them out by specie per encounter
        old_monsters = {monster.name: monster for monster in encounter.monsters}

        # Swap out the old monster for a new one
        for name, monster in old_monsters.items():
            # If there's a forced monster, make sure it gets placed first
            # This COULD be better by not forcing the monster to replace the first one, but that's a meh concern for now
            if forced_monster is not None:
                old_monsters[name] = forced_monster
                available_monsters.remove(forced_monster)
                forced_monster = None
                continue

            picks = [monster for monster in available_monsters if monster.name not in encounter.monster_exclusions]

            # If we're out of monsters to pick from, then reset the list
            if len(picks) == 0:
                available_monsters = get_monsters()
                picks = [monster for monster in available_monsters if monster.name not in encounter.monster_exclusions]

            mon = random.choice(picks)
            old_monsters[name] = mon
            available_monsters.remove(mon)

        # Create a new list of monsters using the swapped out ones
        for monster in encounter.monsters:
            new_monsters.append(old_monsters[monster.name])

    encounter.replace_monsters(*new_monsters)
# endregion


def get_monsters(*monster_exclusions: str) -> List[MonsterData]:
    exclude = list(monster_exclusions) + ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]
    return [monster for monster in monster_data.values() if monster.name not in exclude]


def get_monster(monster_name: str) -> Optional[MonsterData]:
    if monster_data.get(monster_name) is not None:
        return monster_data[monster_name]

    raise KeyError(f"'{monster_name}' was not found in monsters_data")


def get_monsters_with_abilities(*abilities) -> List[MonsterData]:
    return [monster for monster in get_monsters() if set(abilities) & set(monster.groups)]


def get_monsters_in_area(world: World, *areas: str) -> List[MonsterData]:
    monsters: Dict[str, MonsterData] = {}

    for (name, encounter) in world.encounters.items():
        if encounter.area not in areas:
            continue

        for monster in encounter.monsters:
            if monster.name not in monsters:
                monsters[monster.name] = monster

    return list(monsters.values())
