from enum import IntEnum
from typing import Optional, Dict, List
from copy import deepcopy

from BaseClasses import MultiWorld, Location, Region, CollectionState
from worlds.AutoWorld import World
from worlds.monster_sanctuary.rules import AccessCondition


class MonsterSanctuaryLocationCategory(IntEnum):
	CHEST = 0  # Items in chests
	GIFT = 1  # Gifts from NPCs
	MONSTER = 2  # Monsters
	CHAMPION = 3  # Champion battles
	KEEPER = 4  # Keeper battles
	RANK = 5  # Used to track keeper rank gained from battling champions
	FLAG = 10  # Used for events to track location access


class LocationData:
	location_id: int
	name: str
	category: MonsterSanctuaryLocationCategory
	region: str
	default_item: Optional[str]
	access_condition = Optional[AccessCondition]
	encounter_id: Optional[str]
	monster_id: Optional[int]  # 0, 1, or 2. Index of a monster in an encounter
	event: bool

	def __init__(
			self,
			location_id: int,
			name: str,
			region: str,
			category: MonsterSanctuaryLocationCategory,
			default_item: Optional[str] = None,
			access_condition: Optional[AccessCondition] = None,
			encounter_id: Optional[str] = None,
			event: bool = False):
		self.location_id = location_id
		self.name = name
		self.region = region
		self.default_item = default_item
		self.category = category
		self.access_condition = access_condition
		self.encounter_id = encounter_id
		self.event = event


class MonsterSanctuaryLocation(Location):
	game: str = "Monster Sanctuary"

	def __init__(
			self,
			player: int,
			name: str,
			id: Optional[int] = None,
			parent: Optional[Region] = None,
			access_condition: Optional[AccessCondition] = None):
		super().__init__(player, name, id, parent)

		self.access_rule = lambda state: access_condition.has_access(state, player)


# This holds all the location data that is parsed from world.json file
locations_data: Dict[str, LocationData] = {}


def get_champions() -> Dict[str, List[str]]:
	# Key is the region name, value is a list of monster names for that champion encounter
	result: Dict[str, List[Optional[str]]] = {}

	for location_name in locations_data:
		location = locations_data[location_name]
		if location.category != MonsterSanctuaryLocationCategory.CHAMPION:
			continue

		if not result.get(location.region):
			result[location.region] = [None, None, None]

		result[location.region][location.monster_id] = location.default_item

	return result


def add_chest_data(location_id, chest_data, region_name):
	chest_name = f"{region_name}_{chest_data['id']}"

	location = LocationData(
		location_id=location_id,
		name=chest_name,
		region=region_name,
		category=MonsterSanctuaryLocationCategory.CHEST,
		default_item=chest_data["item"],
		access_condition=AccessCondition(chest_data.get("requirements"))
	)

	locations_data[location.name] = location
	return location


def add_gift_data(location_id, gift_data, region_name):
	gift_name = f"{region_name}_{gift_data['id']}"

	location = LocationData(
		location_id=location_id,
		name=gift_name,
		region=region_name,
		category=MonsterSanctuaryLocationCategory.GIFT,
		default_item=gift_data["item"],
		access_condition=AccessCondition(gift_data.get("requirements"))
	)

	locations_data[location.name] = location
	return location


def add_encounter_data(location_id, encounter_data, region_name, category=MonsterSanctuaryLocationCategory.MONSTER):
	result: Dict[int, LocationData] = {}
	encounter_name = f"{region_name}_{encounter_data['id']}"

	# All wild encounters have 3 monster slots, even if it's a champion with only one monster
	# this is so that champion shuffle can shuffle encounters with 3 monsters into locations where
	# normally only 1 monster is present.
	for i in range(3):
		monster_name = None
		if i < len(encounter_data["monsters"]):
			monster_name = encounter_data["monsters"][i]

		location = LocationData(
			location_id=location_id,
			name=f"{encounter_name}_{i}",
			region=region_name,
			category=category,
			default_item=monster_name,
			encounter_id=encounter_name,
			access_condition=AccessCondition(encounter_data.get("requirements"))
		)

		location.monster_id = i

		locations_data[location.name] = location
		result[location_id] = location
		location_id += 1

	return result, location_id


def add_champion_data(location_id, champion_data, region_name):
	event_name = f"{region_name}_Champion"

	rank_event = LocationData(
		location_id=location_id,
		name=event_name,
		region=region_name,
		category=MonsterSanctuaryLocationCategory.RANK,
		default_item=None,
		access_condition=AccessCondition(champion_data.get("requirements"))
	)
	location_id += 1

	new_locations, location_id = add_encounter_data(
		location_id,
		champion_data,
		region_name,
		MonsterSanctuaryLocationCategory.CHAMPION)

	new_locations[rank_event.location_id] = rank_event

	return new_locations, location_id


def add_flag_data(location_id, flag_data, region_name):
	location = LocationData(
		location_id=location_id,
		name=flag_data["id"],
		default_item=flag_data["name"],
		region=region_name,
		category=MonsterSanctuaryLocationCategory.FLAG,
		access_condition=AccessCondition(flag_data.get("requirements"))
	)

	locations_data[location.name] = location
	return location
