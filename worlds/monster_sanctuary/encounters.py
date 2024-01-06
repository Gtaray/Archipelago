from enum import IntEnum
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


class EncounterData:
    encounter_id: int
    name: str
    monsters: List[MonsterData]
    champion: bool = False
    region: str
    access_condition = Optional[AccessCondition]

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
        self.access_condition = access_condition
        self.monsters = []

    def add_monster(self, monster: MonsterData):
        self.monsters.append(monster)


monster_data: Dict[str, MonsterData] = {}
encounter_data: Dict[str, EncounterData] = {}
early_game_areas: List[str] = ["MountainPath", "BlueCave", "KeepersStronghold", "KeepersTower", "StrongholdDungeon", "SnowyPeaks"]
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
def assign_game_stage_to_monsters():
    for encounter_name, encounter in encounter_data.items():
        area = encounter.region.split("_")[0]
        stage: GameStage

        if area in early_game_areas:
            stage = GameStage.EARLY
        elif area in mid_game_areas:
            stage = GameStage.MIDDLE
        elif area in late_game_areas:
            stage = GameStage.LATE

        for monster in encounter.monsters:
            if monster.stage is None or stage < monster.stage:
                monster.stage = stage


def randomize_monsters(world: World) -> None:
    """Randomizes wild monster encounters based on world options"""
    if world.options.randomize_monsters == "no":
        return

    assign_game_stage_to_monsters()

    # if world.options.randomize_champions == 1:
    #     self.champion_data = self.shuffle_dictionary(self.champion_data)
    #
    # # In this case, we randomize champions to literally anything
    # elif self.get_option("randomize_champions") == 2:
    #     for region_name in self.champion_data:
    #         for i in range(len(self.champion_data[region_name])):
    #             if self.champion_data[region_name][i] == "Empty Slot":
    #                 continue
    #             self.champion_data[region_name][i] = ITEMS.get_random_monster_name(self.multiworld)
    #
    # # After setting the champion data above, we go through and add those monsters to the 'used'
    # # in case the 'champions don't appear in the wild' option is enabled.
    # for region_name in self.champion_data:
    #     # For champion fights with more than one monster, we always take the middle one
    #     # which is the second element in the array.
    #     # Champion fights with 1 monster, we take the first element (obviously)
    #     if self.champion_data[region_name][1] == "Empty Slot":
    #         self.champions_used.append(self.champion_data[region_name][0])
    #     else:
    #         self.champions_used.append(self.champion_data[region_name][1])
    #
    # # Remove evolutions from encounter pool if necessary
    # if self.get_option("evolutions_in_wild") == 0:
    #     del self.monsters["G'rulu"]
    #     del self.monsters["Magmamoth"]
    #     del self.monsters["Megataur"]
    #     del self.monsters["Ninki Nanka"]
    #     del self.monsters["Sizzle Knight"]
    #     del self.monsters["Silvaero"]
    #     del self.monsters["Glowdra"]
    #     del self.monsters["Dracogran"]
    #     del self.monsters["Dracozul"]
    #     del self.monsters["Mega Rock"]
    #     del self.monsters["Draconoir"]
    #     del self.monsters["King Blob"]
    #     del self.monsters["Mad Lord"]
    #     del self.monsters["Ascendant"]
    #     del self.monsters["Fumagus"]
    #     del self.monsters["Dracomer"]
    #
    # # Lastly, if we don't want champions to show up in the wild,
    # if self.get_option("champions_in_wild") == 0:
    #     for champion in self.champions_used:
    #         if self.monsters.get(champion) is not None:
    #             del self.monsters[champion]
# endregion


def build_explore_ability_groups() -> Dict:
    item_groups = {}
    for item, data in monster_data.items():
        for group in data.groups:
            item_groups[group] = item_groups.get(group, []) + [item]

    return item_groups

def get_monsters() -> Dict[str, MonsterData]:
    return {monster_name: monster_data[monster_name] for monster_name in monster_data
            if monster_name not in ["Empty Slot",
                                    "Spectral Wolf",
                                    "Spectral Toad",
                                    "Spectral Eagle",
                                    "Spectral Lion",
                                    "Bard"]}


def get_monster(monster_name: str) -> Optional[MonsterData]:
    if monster_data.get(monster_name) is not None:
        return monster_data[monster_name]

    raise KeyError(f"'{monster_name}' was not found in monsters_data")


def get_random_monster_name(multiworld: MultiWorld) -> str:
    valid_items = [item for item in get_monsters()]
    return multiworld.random.choice(valid_items)


def shuffle_dictionary(self, dictionary) -> Dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    self.multiworld.random.shuffle(values)

    # After shuffling the ItemData, we map those now shuffled items
    # back onto the dictionary
    for i in range(len(keys)):
        dictionary[keys[i]] = values[i]

    return dictionary
