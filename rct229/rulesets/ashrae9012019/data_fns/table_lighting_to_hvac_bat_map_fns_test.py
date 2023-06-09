from rct229.rulesets.ashrae9012019.data_fns.table_lighting_to_hvac_bat_map_fns import (
    lighting_to_hvac_bat,
)


def test__lighting_to_hvac_bat__DORMITORY():
    assert lighting_to_hvac_bat("DORMITORY") == "RESIDENTIAL"
