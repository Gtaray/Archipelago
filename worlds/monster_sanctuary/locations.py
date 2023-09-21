from enum import IntEnum
from typing import Optional
from copy import deepcopy

from BaseClasses import MultiWorld, Location, Region
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


class MonsterSanctuaryLocation(Location):
	game: str = "Monster Sanctuary"
	category: MonsterSanctuaryLocationCategory
	access_rule = Optional[AccessCondition]
	default_item: str
	encounter_id: Optional[int] = None
	event: bool

	def __init__(
			self,
			player: int,
			name: str,
			category: MonsterSanctuaryLocationCategory,
			default_item: Optional[str] = None,
			address: Optional[int] = None,
			parent: Optional[Region] = None,
			access_rule: Optional[AccessCondition] = None):
		self.default_item = default_item
		self.category = category
		self.access_rule = access_rule

		super().__init__(player, name, address, parent)

class LocationData:
	id: int
	name: str
	chest_id: int
	region: str
	default_item: Optional[str]
	category: MonsterSanctuaryLocationCategory
	monster_id: int

	def __init__(self, region: str, chest_id: Optional[int], default_item: Optional[str], category: MonsterSanctuaryLocationCategory, monster_id: Optional[int] = None):
		self.chest_id = chest_id
		self.region = region
		self.default_item = default_item
		self.category = category

		self.name = region
		if chest_id is not None:
			self.name += f"_{str(chest_id)}"

		if monster_id is not None:
			self.monsterId = monster_id
			self.name += f"_{str(monster_id)}"

		if category is MonsterSanctuaryLocationCategory.RANK:
			self.name += "_Champion"


def get_champion_locations():
	return [location for location in location_table if location.category == MonsterSanctuaryLocationCategory.CHAMPION]


def get_shuffled_champion_map(world: World):
	orig = []
	shuffled = []

	orig = [location.default_item for location in get_champion_locations()]
	shuffled = deepcopy(orig)
	world.random.shuffle(shuffled)

	return {orig[i]: shuffled[i] for i, _ in enumerate(orig)}


def build_location_ids():
	i = 0
	for location in location_table:
		location.id = 970500 + i
		i += 1


location_table = {
	# region Mountain Path
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_North2", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North2", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North2", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_North2", 2, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North2", 2, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North2", 2, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_North4", 31, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North4", 31, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North4", 31, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_NorthHidden", 2, "Manticorb", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_NorthHidden", 2, "Manticorb", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_NorthHidden", 2, "Manticorb", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center2", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center2", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center2", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center2", 5, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center2", 5, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center2", 5, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center4", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center4", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center4", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_Center5", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center5", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center5", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_West1", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West1", 1, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West1", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_West3", 31, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West3", 31, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West3", 31, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_West4", 2, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West4", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West4", 2, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_West5", 1, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_SnowyEntrance2", 1, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_SnowyEntrance2", 1, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_SnowyEntrance2", 1, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_East1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_East1", 1, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_East1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 2),

	LocationData("MountainPath_North3", 6, "Cestus", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North3", 5, "Vital Ring", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North3", 4, "Kunai", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North3", 3, "Hide", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North5", 9, "Bracelet", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North5", 8, "Gauntlet", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North5", 6, "2x Copper", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North6", 1, "Tome", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North6", 2, "2x Potion", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_North7", 1, "Large Shield", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_NorthHidden", 4, "Harp", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center1", 5, "Diadem", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center2", 3, "Morning Star", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center2", 4, "Orb", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center3", 6, "3x Phoenix Tear", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center3", 7, "Impact Ring", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center3", 8, "Red Gem", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center3", 9, "150 G", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center4", 0, "Bandana", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center4", 4, "Skill Resetter", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center5", 6, "Walnut", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center5", 13, "3x Craft Box", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center6", 2, "Pandora's Box", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center6", 5, "Wizard Hat", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_Center6", 10, "2x Potion", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West1", 4, "Crit Ring", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West2", 19, "100 G", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West2", 22, "3x Smoke Bomb", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West4", 1, "Ribbon", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West4", 3, "Shell", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_West4", 6, "Gauntlet+3", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_WestHidden", 0, "Helmet", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_WestHidden2", 1, "Shift Stone", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("MountainPath_SnowyEntrance2", 14, "Mana Ring+3", MonsterSanctuaryLocationCategory.CHEST),

	LocationData("MountainPath_West6", 134, "Mountain Path Key", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("MountainPath_West6", 135, "2x Apple", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("MountainPath_West6", 136, "2x Potato", MonsterSanctuaryLocationCategory.GIFT),

	LocationData("MountainPath_West6", 3, "Golem", MonsterSanctuaryLocationCategory.CHAMPION, 0),
	LocationData("MountainPath_Center7", 1, "Monk", MonsterSanctuaryLocationCategory.CHAMPION, 0),

	LocationData("MountainPath_West6", 2, "Blob", MonsterSanctuaryLocationCategory.KEEPER, 0),
	LocationData("MountainPath_West6", 2, "Blob", MonsterSanctuaryLocationCategory.KEEPER, 1),
	LocationData("MountainPath_West6", 2, "Blob", MonsterSanctuaryLocationCategory.KEEPER, 2),
	# endregion

	# region Keeper Stronghold
	LocationData("KeeperStronghold_WestStairwell", 5, "Staff", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("KeeperStronghold_WestTowers", 4, "Hide+1", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("KeeperStronghold_Storage", 5, "Skill Resetter", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("KeeperStronghold_Storage", 6, "Cape", MonsterSanctuaryLocationCategory.CHEST),

	LocationData("KeeperStronghold_Smith", 290, "2x Copper", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_Smith", 291, "2x Cotton", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_Smith", 292, "Reg Gem", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_Smith", 293, "Green Gem", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_Smith", 294, "Blue Gem", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 326, "Brooch", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 2800011, "Reward Box Lvl 1", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 2800021, "Reward Box Lvl 2", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 2800022, "Reward Box Lvl 3", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 2800023, "Reward Box Lvl 4", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 2800024, "3x Craft Box", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("KeeperStronghold_ParentsRoom", 403, "3x Small Potion", MonsterSanctuaryLocationCategory.GIFT),
	# endregion

	# region Blue Caves
	LocationData("BlueCave_StrongholdEntrance", 6, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("BlueCave_StrongholdEntrance", 6, "Grummy", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("BlueCave_StrongholdEntrance", 6, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("BlueCave_Switches", 6, "Grummy", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("BlueCave_Switches", 6, "Grummy", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("BlueCave_Switches", 6, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("BlueCave_NorthFork", 6, "Fungi", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("BlueCave_NorthFork", 6, "Grummy", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("BlueCave_NorthFork", 6, "Fungi", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("BlueCave_NorthFork", 9, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("BlueCave_NorthFork", 9, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("BlueCave_NorthFork", 9, "Tengu", MonsterSanctuaryLocationCategory.MONSTER, 2),


	# LocationData("BlueCave_StrongholdEntrance", 2, "???", MonsterSanctuaryLocationCategory.CHEST), # Bravery chest
	LocationData("BlueCave_Platforms", 0, "Blue Caves Key", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_Platforms", 1, "250 G", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_Platforms", 3, "Bracelet+1", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_NorthFork", 4, "Katar", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_NorthFork", 7, "Ribbon+2", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_NorthFork", 10, "Cape+2", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_NorthFork", 11, "Bracelet+2", MonsterSanctuaryLocationCategory.CHEST),
	LocationData("BlueCave_NorthFork", 12, "Corn", MonsterSanctuaryLocationCategory.CHEST),

	LocationData("BlueCave_Switches", None, None, MonsterSanctuaryLocationCategory.FLAG),
	# endregion

	# region Champion Events
	LocationData("MountainPath_West6", None, "Steam Golem", MonsterSanctuaryLocationCategory.RANK),
	LocationData("MountainPath_Center7", None, "Monk", MonsterSanctuaryLocationCategory.RANK),
	# endregion
}
