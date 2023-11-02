from typing import Dict, List, Optional

from BaseClasses import MultiWorld
from worlds.monster_sanctuary.rules import AccessCondition


class MonsterData:
    id: int
    name: str
    groups: List[str]


class EncounterData:
    id: int
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
                 access_condition: Optional[AccessCondition] = None):
        self.id = encounter_id
        self.name = encounter_name
        self.champion = is_champion
        self.region = region
        self.access_condition = access_condition

    def add_monster(self, monster: MonsterData):
        self.monsters.append(monster)


monsters_data: Dict[str, MonsterData]
encounters_data: Dict[str, EncounterData]


# region Data Loading
def add_encounter_data(encounter_data, region_name) -> Optional[EncounterData]:
    encounter_id = encounter_data.get('id')
    encounter: EncounterData
    if isinstance(encounter_data, str):
        return None
    encounter_name = f"{region_name}_{encounter_id}"

    encounter = EncounterData(
        encounter_id=encounter_id,
        encounter_name=encounter_name,
        is_champion=False,
        region=region_name,
        access_condition=AccessCondition(encounter_data.get("requirements"))
    )

    # All wild encounters have 3 monster slots, even if it's a champion with only one monster
    # this is so that champion shuffle can shuffle encounters with 3 monsters into locations where
    # normally only 1 monster is present.
    for i in range(3):
        monster_name = None
        if encounter_data.get("monsters") is None:
            breakpoint()

        if i < len(encounter_data.get("monsters")):
            monster_name = encounter_data.get("monsters")[i]
        else:
            monster_name = "Empty Slot"

        monster = get_monster(monster_name)
        if monster is not None:
            encounter.add_monster(monster)

    if encounters_data.get(encounter.name) is not None:
        raise KeyError(f"{encounter.name} already exists in encounters_data")

    encounters_data[encounter.name] = encounter

    return encounter


def add_champion_data(location_id, champion_data, region_name) -> (Dict[int, LocationData], int):
    event_name = f"{region_name}_Champion"

    rank_event = LocationData(
        location_id=location_id,
        name=event_name,
        region=region_name,
        category=MonsterSanctuaryLocationCategory.RANK,
        default_item="Champion Defeated",
        access_condition=AccessCondition(champion_data.get("requirements"))
    )
    locations_data[rank_event.name] = rank_event
    location_id += 1

    new_locations, location_id = add_encounter_data(
        location_id,
        champion_data,
        region_name,
        MonsterSanctuaryLocationCategory.CHAMPION)

    new_locations[rank_event.location_id] = rank_event

    return new_locations, location_id


# endregion


def get_monsters() -> Dict[str, MonsterData]:
    return {monster_name: monsters_data[monster_name] for monster_name in monsters_data
            if monster_name not in ["Empty Slot",
                                    "Spectral Wolf",
                                    "Spectral Toad",
                                    "Spectral Eagle",
                                    "Spectral Lion",
                                    "Bard"]}


def get_monster(monster_name: str) -> Optional[MonsterData]:
    if monsters_data.get(monster_name) is not None:
        return monsters_data[monster_name]

    raise KeyError(f"'{monster_name}' was not found in monsters_data")


def get_random_monster_name(multiworld: MultiWorld) -> str:
    valid_items = [item for item in get_monsters()]
    return multiworld.random.choice(valid_items)
