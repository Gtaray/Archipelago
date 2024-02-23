from enum import IntEnum
from typing import Optional, Dict, List

from BaseClasses import Location, Region
from worlds.monster_sanctuary.rules import AccessCondition


class MonsterSanctuaryLocationCategory(IntEnum):
	CHEST = 0  # Items in chests
	GIFT = 1  # Gifts from NPCs
	SHOP = 2  # Items in an NPC shop
	RANK = 5  # Used to track keeper rank gained from battling champions


class LocationData:
	location_id: int
	name: str
	category: MonsterSanctuaryLocationCategory
	region: str
	default_item: Optional[str]
	access_condition = Optional[AccessCondition]
	object_id: Optional[int]
	monster_id: Optional[int]  # 0, 1, or 2. Index of a monster in an encounter
	event: bool
	postgame: bool = False
	hint: Optional[str]
	shop_is_limited: bool = False
	logical_name: str = ""

	def __init__(
			self,
			location_id: int,
			name: str,
			region: str,
			category: MonsterSanctuaryLocationCategory,
			default_item: Optional[str] = None,
			access_condition: Optional[AccessCondition] = None,
			object_id: Optional[int] = None,
			event: bool = False,
			hint: Optional[str] = None):
		self.location_id = location_id
		self.name = name
		self.region = region
		self.default_item = default_item
		self.category = category
		self.access_condition = access_condition
		self.object_id = object_id
		self.event = event
		self.hint = hint
		self.logical_name = ""


class MonsterSanctuaryLocation(Location):
	game: str = "Monster Sanctuary"

	def __init__(
			self,
			player: int,
			name: str,
			logical_name: str,
			address: Optional[int] = None,
			parent: Optional[Region] = None,
			access_condition: Optional[AccessCondition] = None):
		super().__init__(player, name, address, parent)

		self.logical_name = logical_name
		self.access_rule = lambda state: access_condition is None or access_condition.has_access(state, player)

		data = location_data.get(name)
		if data is None:
			return
		if data.hint is not None:
			self._hint_text = data.hint


# This holds all the location data that is parsed from world.json file
location_data: Dict[str, LocationData] = {}


def add_location(key: str, location: LocationData) -> None:
	if location_data.get(location.name) is not None:
		raise KeyError(f"{location.name} already exists in locations_data")

	location_data[key] = location


def clear_data():
	location_data.clear()


def set_postgame_location(location_name: str, is_postgame: bool = True):
	if location_data.get(location_name) is None:
		raise KeyError("f{location_name} does not exist")

	location_data[location_name].postgame = is_postgame


def is_location_type(location: str, *types: MonsterSanctuaryLocationCategory) -> bool:
	data = location_data[location]
	return data.category in types


def get_locations_of_type(*categories: MonsterSanctuaryLocationCategory):
	return [location_data[name] for name in location_data if location_data[name].category in categories]


def is_location_shop(location: str) -> bool:
	return location in location_data and location_data[location].category == MonsterSanctuaryLocationCategory.SHOP


def is_shop_limited(location: str) -> bool:
	return location_data[location].shop_is_limited


def get_location_name_for_client(name: str) -> Optional[str]:
	if name not in location_data:
		return None

	data = location_data[name]
	parts = name.split('_')

	# We reconstruct the location name without the subdivision,
	# which is what the game client will use
	trimmed_name = f"{parts[0]}_{parts[1]}"
	if data.object_id is not None:
		trimmed_name += f"_{data.object_id}"

	if data.category == MonsterSanctuaryLocationCategory.RANK:
		trimmed_name += "_Champion"

	return trimmed_name
