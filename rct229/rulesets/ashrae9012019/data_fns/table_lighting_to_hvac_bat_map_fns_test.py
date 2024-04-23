from rct229.rulesets.ashrae9012019.data_fns.table_lighting_to_hvac_bat_map_fns import (
    building_lighting_to_hvac_bat,
    space_lighting_to_hvac_bat,
)


def test__lighting_to_hvac_bat__DORMITORY():
    assert building_lighting_to_hvac_bat("DORMITORY") == "RESIDENTIAL"


def test__space_lighting_to_hvac_bat__ATRIUM_HIGH():
    assert space_lighting_to_hvac_bat("ATRIUM_HIGH") == "OTHER_UNDETERMINED"
