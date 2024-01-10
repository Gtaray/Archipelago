from enum import IntEnum
from random import Random
from typing import Dict, List, Optional

from .rules import AccessCondition
from BaseClasses import MultiWorld
from ..AutoWorld import World


class GameStage(IntEnum):
    EARLY = 0
    MIDDLE = 1
    LATE = 2


class MonsterData:
    id: int
    name: str
    groups: List[str]
    stage: Optional[GameStage] = None

    def __init__(self, id: int, name: str, groups: List[str]):
        # This needs to exist alongside normal item ids, because monsters will ultimately be classified as items
        # Because event locations need to hold items with ids
        self.id = id
        self.name = name
        self.groups = groups

    def __str__(self):
        return self.name


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

species_swap: Dict[str, MonsterData] = {}  # tracks of which species are swapped when randomizing monsters by specie

early_game_areas: List[str] = ["MountainPath", "BlueCave", "KeepersStronghold", "KeepersTower", "StrongholdDungeon",
                               "SnowyPeaks"]
mid_game_areas: List[str] = ["SunPalace", "AncientWoods", "HorizonBeach", "MagmaChamber", "BlobBurg"]
late_game_areas: List[str] = ["ForgottenWorld", "MysticalWorkshop", "Underworld", "AbandonedTower", "EternitysEnd"]


# region Data Loading
def add_encounter(encounter: EncounterData, monsters: List[str]) -> None:
    if encounter_data.get(encounter.name) is not None:
        raise KeyError(f"{encounter.name} already exists in encounters_data")

    for monster_name in monsters:
        encounter.add_monster(get_monster(monster_name))

    encounter_data[encounter.name] = encounter


# endregion


# region Monster and Champion Randomization
def randomize_monsters(world: World) -> None:
    if world.options.randomize_monsters == "no":
        return

    assign_game_stage_to_monsters()
    set_encounter_monster_exclusions(world)

    random = world.multiworld.random
    encounters_to_randomize = [encounter for name, encounter in encounter_data.items()]
    available_monsters = get_monsters()

    # if shuffling, then we shuffle the species
    # if not shuffling, then we place the required monsters
    if world.options.randomize_monsters == "by_specie":
        shuffle_species(world)

        for name, encounter in encounter_data.items():
            encounter.replace_monsters(*[species_swap[monster.name] for monster in encounter.monsters])

    else:
        # Start by hard-placing some monsters to ensure that certain abilities show
        def place_ability_in_area(abilities: List[str], areas: List[str]):
            new_monsters = []
            encounter = random.choice(get_encounters_in_area(*areas))
            new_monster = random.choice([mon for mon in available_monsters if set(abilities) & set(mon.groups)])

            replace_monsters_in_encounter(world, encounter, available_monsters, new_monster)

            encounter.replace_monsters(*new_monsters)
            encounters_to_randomize.remove(encounter)
            available_monsters.remove(new_monster)

        place_ability_in_area(["Breakable Walls"], ["MountainPath", "BlueCave"])
        place_ability_in_area(["Flying"], ["MountainPath", "BlueCave"])
        place_ability_in_area(
            ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"],
            ["MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace"])

    # We've either shuffled the monster dictionary (if set to shuffle)
    # Or placed necessary monsters into areas (if set to a different randomize setting)
    # Now we just go through each encounter left and randomize them.
    for encounter in encounters_to_randomize:
        replace_monsters_in_encounter(world, encounter, available_monsters)


def assign_game_stage_to_monsters():
    for encounter_name, encounter in encounter_data.items():
        stage: GameStage

        if encounter.area in early_game_areas:
            stage = GameStage.EARLY
        elif encounter.area in mid_game_areas:
            stage = GameStage.MIDDLE
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

    # Get a list of regions where improved mobility abilities must be limited
    improved_mobility_area_limit = []
    if world.options.improved_mobility_limit == "midgame":
        improved_mobility_area_limit = early_game_areas
    elif world.options.improved_mobility_limit == "lategame":
        improved_mobility_area_limit = early_game_areas + mid_game_areas

    # if there's regions where improved mobility are illegal, set it up.
    if len(improved_mobility_area_limit) > 0:
        encounters = [encounter for encounter in encounter_data.values()
                      if encounter.area in improved_mobility_area_limit]
        monsters = [monster.name for monster in get_monsters_with_abilities(
            "Improved Flying", "Lofty Mount", "Improved Swimming", "Dual Mobility")]
        for encounter in encounters:
            encounter.add_exclusion(*monsters)


def shuffle_species(world: World):
    """Shuffles the monster specie dictionary, adhering to all the relevant monster placement rules"""
    if world.options.randomize_monsters != "by_specie":
        return

    random = world.multiworld.random
    available_monsters = get_monsters()

    # These monsters should never be shuffled
    species_swap["Spectral Wolf"] = get_monster("Spectral Wolf")
    species_swap["Spectral Toad"] = get_monster("Spectral Toad")
    species_swap["Spectral Eagle"] = get_monster("Spectral Eagle")
    species_swap["Spectral Lion"] = get_monster("Spectral Lion")
    species_swap["Bard"] = get_monster("Bard")

    # Start by placing necessary monsters
    def place_ability_in_area(abilities: List[str], areas: List[str]):
        # Pick a monster that hasn't already been shuffled, and is in the right areas
        # then swap it with a new monster that has the correct ability
        original_monster = random.choice([mon for mon in get_monsters_in_area(*areas)
                                          if mon.name not in species_swap])
        new_monster = random.choice([mon for mon in available_monsters
                                     if set(abilities) & set(mon.groups)])

        species_swap[original_monster.name] = new_monster
        available_monsters.remove(new_monster)

    place_ability_in_area(["Breakable Walls"], ["MountainPath", "BlueCave"])
    place_ability_in_area(["Flying"], ["MountainPath", "BlueCave"])
    place_ability_in_area(
        ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"],
        ["MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace"])

    # Then shuffle monsters that have limited options based on exclusions in encounters
    def place_monsters_in_encounter_with_exclusions(encounter: EncounterData):
        for original_monster in encounter.monsters:
            # If we've already swapped this monster, then ignore it and move on
            if original_monster.name in species_swap:
                continue

            available = [mon for mon in available_monsters if mon.name not in encounter.monster_exclusions]
            new_monster = random.choice(available)
            species_swap[original_monster.name] = new_monster
            available_monsters.remove(new_monster)

    for name, enc in encounter_data.items():
        if len(enc.monster_exclusions) > 0:  # Ignore encounters with no exclusions
            place_monsters_in_encounter_with_exclusions(enc)

    # Shuffle the remainder of available monsters
    keys = [monster.name for monster in get_monsters() if monster.name not in species_swap]
    values = available_monsters
    random.shuffle(values)
    for i in range(len(keys)):
        species_swap[keys[i]] = values[i]

    if len(species_swap) != len(monster_data):
        for monster in [name for name in monster_data if name not in species_swap]:
            print(f"WARNING: {monster} was not swapped")


def replace_monsters_in_encounter(world: World, encounter: EncounterData, available_monsters: List[MonsterData],
                                  forced_monster: Optional[MonsterData] = None):
    random = world.multiworld.random
    new_monsters = []

    if world.options.randomize_monsters == "yes":
        # Fill out the rest of the monster slots with random monsters
        if forced_monster is not None:
            new_monsters.append(forced_monster)
            available_monsters.remove(forced_monster)

        while len(new_monsters) < len(encounter.monsters):
            mon = random.choice([monster for monster in available_monsters
                           if monster.name not in encounter.monster_exclusions])
            new_monsters.append(mon)
            available_monsters.remove(mon)

        # Finally, shuffle the monsters for good measure
        world.multiworld.random.shuffle(new_monsters)

    elif world.options.randomize_monsters == "by_specie":
        # We've already swapped species, so all we need to do is add the swapped mons to the list
        # So it can get replaced later.
        for monster in encounter.monsters:
            new_monsters.append(species_swap[monster.name])

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

            mon = random.choice([monster for monster in available_monsters
                           if monster.name not in encounter.monster_exclusions])
            old_monsters[name] = mon
            available_monsters.remove(mon)

        # Create a new list of monsters using the swapped out ones
        for i in range(len(encounter.monsters)):
            new_monsters[i] = old_monsters[encounter.monsters[i].name]

    encounter.replace_monsters(*new_monsters)
# endregion


def build_explore_ability_groups() -> Dict:
    item_groups = {}
    for item, data in monster_data.items():
        for group in data.groups:
            item_groups[group] = item_groups.get(group, []) + [item]

    return item_groups


def get_monsters(*monster_exclusions: str) -> List[MonsterData]:
    exclude = list(monster_exclusions) + ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]
    return [monster for monster in monster_data.values() if monster.name not in exclude]


def get_monster(monster_name: str) -> Optional[MonsterData]:
    if monster_data.get(monster_name) is not None:
        return monster_data[monster_name]

    raise KeyError(f"'{monster_name}' was not found in monsters_data")


def get_monsters_with_abilities(*abilities) -> List[MonsterData]:
    return [monster for monster in get_monsters() if set(abilities) & set(monster.groups)]


def get_random_monster_with_ability(random: Random, *abilities) -> MonsterData:
    monsters = get_monsters_with_abilities(*abilities)
    return random.choice(monsters)


def get_monsters_in_area(*areas: str) -> List[MonsterData]:
    monsters: Dict[str, MonsterData] = {}

    for (name, encounter) in encounter_data.items():
        if encounter.area not in areas:
            continue

        for monster in encounter.monsters:
            if monster.name not in monsters:
                monsters[monster.name] = monster

    return list(monsters.values())


def get_random_monster_name(multiworld: MultiWorld) -> str:
    valid_items = [item for item in get_monsters()]
    return multiworld.random.choice(valid_items).name


def get_encounters_in_area(*areas: str) -> List[EncounterData]:
    return [encounter for (name, encounter) in encounter_data.items()
            if encounter.area in areas]


def get_random_encounter_in_area(random: Random, *areas: str) -> EncounterData:
    return random.choice(get_encounters_in_area(*areas))
