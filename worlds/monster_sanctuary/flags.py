def add_flag_data(location_id, flag_data, region_name) -> LocationData:
	location = LocationData(
		location_id=location_id,
		name=flag_data["id"],
		default_item=flag_data["name"],
		region=region_name,
		category=MonsterSanctuaryLocationCategory.FLAG,
		access_condition=AccessCondition(flag_data.get("requirements"))
	)

	if locations_data.get(location.name) is not None:
		raise KeyError(f"{location.name} already exists in locations_data")

	locations_data[location.name] = location
	return location