from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_total_lab_exhaust_from_zone_exhaust_fans import (
    get_building_total_lab_exhaust_from_zone_exhaust_fans,
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
                                {
                                    "id": "Space 1",
                                    "function": "LABORATORY",
                                },
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "function": "LABORATORY",
                                },
                                {
                                    "id": "Space 3",
                                    "function": "KITCHEN",
                                },
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 2",
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 3",
                            "spaces": [
                                {
                                    "id": "Space 4",
                                    "function": "LABORATORY",
                                },
                                {
                                    "id": "Space 5",
                                },
                            ],
                        },
                        {
                            "id": "Thermal Zone 4",
                            "spaces": [
                                {
                                    "id": "Space 6",
                                    "function": "KITCHEN",
                                },
                                {
                                    "id": "Space 7",
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


def test__get_building_total_lab_exhaust_from_zone_exhaust_fan__success():
    assert get_building_total_lab_exhaust_from_zone_exhaust_fans(
        TEST_RMD_UNIT
    ) == 1000 * ureg("liter / second").to("ft^3 / min")
