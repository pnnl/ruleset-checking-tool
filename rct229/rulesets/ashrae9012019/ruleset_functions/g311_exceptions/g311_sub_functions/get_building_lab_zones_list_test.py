from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_lab_zones_list import (
    get_building_lab_zones_list,
)
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
                        {
                            "id": "Thermal Zone 5",
                            "spaces": [
                                {
                                    "id": "Space 8",
                                    "lighting_space_type": "LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM",
                                },
                            ],
                        },
                        {
                            "id": "Thermal Zone 6",
                            "spaces": [
                                {
                                    "id": "Space 9",
                                    "function": "LABORATORY",
                                    "lighting_space_type": "LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM",
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


def test__get_building_lab_zone_list__success():
    assert get_building_lab_zones_list(TEST_RMD_UNIT) == [
        "Thermal Zone 1",
        "Thermal Zone 2",
        "Thermal Zone 3",
        "Thermal Zone 5",
        "Thermal Zone 6",
    ]
