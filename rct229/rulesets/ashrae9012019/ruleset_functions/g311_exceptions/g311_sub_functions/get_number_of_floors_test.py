from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_number_of_floors import (
    get_number_of_floors,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI_HAS_NOF = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "number_of_floors_above_grade": 1,
            "number_of_floors_below_grade": 1,
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMI_FLOOR_NAMES = {
    "id": "ASHRAE229",
    "ruleset_model_descriptions": [
        {
            "id": "RMR 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Zone 1",
                                    "floor_name": "test floor 1",
                                    "spaces": [
                                        {
                                            "id": "Space 1",
                                            "lighting_space_type": "DWELLING_UNIT",
                                            "floor_area": 10,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "Terminal 1",
                                            "served_by_heating_ventilating_air_conditioning_system": "HVAC 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Zone 2",
                                    "floor_name": "test floor 2",
                                    "spaces": [
                                        {
                                            "id": "Space 2",
                                            "lighting_space_type": "DWELLING_UNIT",
                                            "floor_area": 4,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "Terminal 2",
                                            "served_by_heating_ventilating_air_conditioning_system": "HVAC 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Zone 3",
                                    "floor_name": "test floor 3",
                                    "spaces": [
                                        {
                                            "id": "Space 3",
                                            "lighting_space_type": "PARKING_AREA_INTERIOR",
                                            "floor_area": 4,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "Terminal 3",
                                            "served_by_heating_ventilating_air_conditioning_system": "HVAC 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Zone 4",
                                    "floor_name": "test floor 4",
                                    "spaces": [
                                        {
                                            "id": "Space 4",
                                            "lighting_space_type": "PARKING_AREA_INTERIOR",
                                            "floor_area": 2,
                                        },
                                        {
                                            "id": "Space 5",
                                            "lighting_space_type": "DWELLING_UNIT",
                                            "floor_area": 2,
                                        },
                                    ],
                                    "terminals": [
                                        {
                                            "id": "Terminal 4",
                                            "served_by_heating_ventilating_air_conditioning_system": "HVAC 1",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "HVAC 1",
                                    "cooling_system": {
                                        "id": "Cooling System 1",
                                        "design_sensible_cool_capacity": 17585.0,
                                    },
                                    "heating_system": {
                                        "id": "Heating System 1",
                                        "design_capacity": 10257.488888888889,
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
            "type": "BASELINE_0",
        }
    ],
    "data_timestamp": "2024-02-12T09:00Z",
}


TEST_RPD_HAS_NOF = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMI_HAS_NOF],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD_HAS_NOF_UNIT = quantify_rmr(TEST_RPD_HAS_NOF)["ruleset_model_descriptions"][0]
TEST_RMD_FLOOR_NAMES_UNIT = quantify_rmr(TEST_RMI_FLOOR_NAMES)[
    "ruleset_model_descriptions"
][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMI_FLOOR_NAMES)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_number_of_floors_with_nof():
    assert get_number_of_floors("CZ0A", TEST_RMD_HAS_NOF_UNIT) == 2


def test__get_number_of_floors_with_floor_names():
    assert get_number_of_floors("CZ0A", TEST_RMD_FLOOR_NAMES_UNIT) == 3
