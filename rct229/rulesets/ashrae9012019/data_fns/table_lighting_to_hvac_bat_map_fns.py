from rct229.rulesets.ashrae9012019.data import data
from rct229.utils.assertions import assert_


def building_lighting_to_hvac_bat(lighting_bat):
    bat_conversion_table = data["ashrae_90_1_lighting_to_hvac_map"]
    assert_(
        lighting_bat in bat_conversion_table,
        f"Lighting area type {lighting_bat} does not exist in ashrae_90_1_lighting_to_hvac_map",
    )
    return bat_conversion_table[lighting_bat]


def space_lighting_to_hvac_bat(lighting_bat):
    bat_conversion_table = data["ashrae_90_1_space_lighting_to_hvac_map"]
    assert_(
        lighting_bat in bat_conversion_table,
        f"Lighting area type {lighting_bat} does not exist in ashrae_90_1_lighting_to_hvac_map",
    )
    return bat_conversion_table[lighting_bat]
