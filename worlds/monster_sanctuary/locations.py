from enum import IntEnum
from typing import Optional

from BaseClasses import MultiWorld, Location, Region

class MonsterSanctuaryLocationCategory(IntEnum):
	ITEM = 0
	GIFT = 1
	MONSTER = 2
	CHAMPION = 3


class LocationData:
	id: int
	name: str
	chestId: int
	region: str
	default_item: str
	category: MonsterSanctuaryLocationCategory
	monsterId: int

	def __init__(self, region: str, chestId: int, default_item: str, category: MonsterSanctuaryLocationCategory, monsterId: int = None):
		self.chestId = chestId
		self.region = region
		self.default_item = default_item
		self.category = category

		self.name = region + "_" + str(chestId)
		if monsterId is not None:
			self.monsterId = monsterId
			self.name += str(monsterId)


class MonsterSanctuaryLocation(Location):
	game: str = "Monster Sanctuary"
	category: MonsterSanctuaryLocationCategory
	default_item: str

	def __init__(
			self,
			player: int,
			name: str,
			category: MonsterSanctuaryLocationCategory,
			default_item: str,
			address: Optional[int] = None,
			parent: Optional[Region] = None):
		super().__init__(player, name, address, parent)
		self.default_item = default_item
		self.category = category


def build_location_ids():
	i = 0
	for location in location_table:
		location.id = 970500 + i
		i += 1


location_table = {
	# Mountain Path
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North1", 0, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 2),
	LocationData("MountainPath_North2", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North2", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North2", 2, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North2", 2, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_North4", 31, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_North4", 31, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_NorthHidden", 2, "Manticorb", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_NorthHidden", 2, "Manticorb", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center1", 1, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center2", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center2", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center2", 5, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center2", 5, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center4", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center4", 1, "Rocky", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_Center5", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_Center5", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West1", 1, "Blob", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West1", 1, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West3", 31, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West3", 31, "Vaero", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West4", 2, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West4", 2, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West5", 1, "Catzerker", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_West5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_West5", 1, "Magmapillar", MonsterSanctuaryLocationCategory.MONSTER, 1),
	LocationData("MountainPath_SnowyEntrance2", 1, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 0),
	LocationData("MountainPath_SnowyEntrance2", 1, "Yowie", MonsterSanctuaryLocationCategory.MONSTER, 1),

	LocationData("MountainPath_North3", 6, "Cestus", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North3", 5, "Vital Ring", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North3", 4, "Kunai", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North3", 3, "Hide", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North5", 9, "Bracelet", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North5", 8, "Gauntlet", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North5", 6, "Copper x2", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North6", 1, "Tome", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North6", 2, "Potion x2", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_North7", 1, "Large Shield", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_NorthHidden", 4, "Harp", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center1", 5, "Diadem", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center3", 6, "Phoenix Tear x3", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center3", 7, "Impact Ring", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center3", 8, "Red Gem", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center3", 9, "150 G", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center4", 0, "Bandana", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center4", 4, "Skill Resetter", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center5", 6, "Walnut", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center5", 3, "Craft Box x3", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center6", 2, "Pandora's Box", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center6", 5, "Wizard Hat", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_Center6", 0, "Potion x2", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West1", 4, "Crit Ring", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West2", 9, "100 G", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West2", 2, "Smoke Bomb x3", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West4", 1, "Ribbon", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West4", 3, "Shell", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_West4", 6, "Gauntlet +3", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_WestHidden", 0, "Helmet", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_WestHidden2", 1, "Shift Stone", MonsterSanctuaryLocationCategory.ITEM),
	LocationData("MountainPath_SnowyEntrance2", 4, "Mana Ring +3", MonsterSanctuaryLocationCategory.ITEM),

	LocationData("MountainPath_West6", 0, "Mountain Path Key", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("MountainPath_West6", 1, "Apple x2", MonsterSanctuaryLocationCategory.GIFT),
	LocationData("MountainPath_West6", 2, "Potato x2", MonsterSanctuaryLocationCategory.GIFT),

	LocationData("MountainPath_West6", 3, "Golem", MonsterSanctuaryLocationCategory.CHAMPION, 0),
	LocationData("MountainPath_Center7", 1, "Monk", MonsterSanctuaryLocationCategory.CHAMPION, 0),
}