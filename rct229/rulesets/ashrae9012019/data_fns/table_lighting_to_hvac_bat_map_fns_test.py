from rct229.rulesets.ashrae9012019.data_fns.table_lighting_to_hvac_bat_map_fns import (
    building_lighting_to_hvac_bat,
)


def test__lighting_to_hvac_bat__ATRIUM_HIGH():
    assert building_lighting_to_hvac_bat("ATRIUM_HIGH") == "UNDETERMINED"


def test__space_lighting_to_hvac_bat__AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER():
    assert (
        building_lighting_to_hvac_bat("AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER")
        == "ALL_OTHER"
    )
