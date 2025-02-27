from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_hvac_bat import (
    get_zone_hvac_bat_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                # ATRIUM_LOW_MEDIUM - OTHER_UNDETERMINED
                                {
                                    "id": "Space 1",
                                    "floor_area": 100,
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                },
                                {
                                    "id": "Space 2",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                },
                                # JUDGES_CHAMBERS "OTHER_NON_RESIDENTIAL"
                                {
                                    "id": "Space 3",
                                    "floor_area": 200,
                                    "lighting_space_type": "JUDGES_CHAMBERS",
                                },
                                # SEATING_AREA_GENERAL PUBLIC_ASSEMBLY
                                {
                                    "id": "Space 4",
                                    "floor_area": 0,
                                    "lighting_space_type": "SEATING_AREA_GENERAL",
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "type": "BASELINE_0",
}


TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__zone_hvac_bat__success():
    assert get_zone_hvac_bat_dict(TEST_RMD_UNIT, "Thermal Zone 1") == {
        "OTHER_UNDETERMINED": 100 * ureg("m2").to("ft**2"),
        "OTHER_NON_RESIDENTIAL": 200 * ureg("m2").to("ft**2"),
        "PUBLIC_ASSEMBLY": 0.0 * ureg("ft**2"),
    }
