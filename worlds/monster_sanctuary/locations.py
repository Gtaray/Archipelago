from enum import IntEnum
from typing import Optional, Dict, List

from BaseClasses import Location, Region
from worlds.monster_sanctuary.rules import AccessCondition


class MonsterSanctuaryLocationCategory(IntEnum):
	CHEST = 0  # Items in chests
	GIFT = 1  # Gifts from NPCs
	RANK = 5  # Used to track keeper rank gained from battling champions


class LocationData:
	location_id: int
	name: str
	category: MonsterSanctuaryLocationCategory
	region: str
	default_item: Optional[str]
	access_condition = Optional[AccessCondition]
	object_id: Optional[str]
	monster_id: Optional[int]  # 0, 1, or 2. Index of a monster in an encounter
	event: bool
	postgame: bool = False
	hint: Optional[str]

	def __init__(
			self,
			location_id: int,
			name: str,
			region: str,
			category: MonsterSanctuaryLocationCategory,
			default_item: Optional[str] = None,
			access_condition: Optional[AccessCondition] = None,
			object_id: Optional[str] = None,
			event: bool = False,
			hint: Optional[str]=None):
		self.location_id = location_id
		self.name = name
		self.region = region
		self.default_item = default_item
		self.category = category
		self.access_condition = access_condition
		self.object_id = object_id
		self.event = event
		self.hint = hint


class MonsterSanctuaryLocation(Location):
	game: str = "Monster Sanctuary"

	def __init__(
			self,
			player: int,
			name: str,
			address: Optional[int] = None,
			parent: Optional[Region] = None,
			access_condition: Optional[AccessCondition] = None):
		super().__init__(player, name, address, parent)

		self.access_rule = lambda state: access_condition.has_access(state, player)

		data = locations_data.get(name)
		if data is None:
			return
		if data.hint is not None:
			self._hint_text = data.hint


# This holds all the location data that is parsed from world.json file
locations_data: Dict[str, LocationData] = {}


def clear_data():
	locations_data.clear()


def is_location_type(location: str, *types: MonsterSanctuaryLocationCategory) -> bool:
	data = locations_data[location]
	return data.category in types


def get_locations_of_type(*categories: MonsterSanctuaryLocationCategory):
	return [locations_data[name] for name in locations_data if locations_data[name].category in categories]


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


def add_chest_data(location_id, chest_data, region_name) -> LocationData:
	chest_name = f"{region_name}_{chest_data['id']}"

	if chest_data.get("item") is None:
		breakpoint()

	location = LocationData(
		location_id=location_id,
		name=chest_name,
		region=region_name,
		category=MonsterSanctuaryLocationCategory.CHEST,
		default_item=chest_data["item"],
		access_condition=AccessCondition(chest_data.get("requirements")),
		object_id=chest_data["id"],
		hint=chest_data.get("hint")
	)

	if locations_data.get(location.name) is not None:
		raise KeyError(f"{location.name} already exists in locations_data")

	locations_data[location.name] = location
	return location


def add_gift_data(location_id, gift_data, region_name) -> LocationData:
	gift_name = f"{region_name}_{gift_data['id']}"

	location = LocationData(
		location_id=location_id,
		name=gift_name,
		region=region_name,
		category=MonsterSanctuaryLocationCategory.GIFT,
		default_item=gift_data["item"],
		access_condition=AccessCondition(gift_data.get("requirements")),
		object_id=gift_data["id"],
	)

	if locations_data.get(location.name) is not None:
		raise KeyError(f"{location.name} already exists in locations_data")

	locations_data[location.name] = location
	return location

