from copy import deepcopy

from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_predominant_hvac_building_area_type import (
    get_predominant_hvac_building_area_type,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)

POWER_DELTA = 1
POWER_THRESHOLD_100 = (CAPACITY_THRESHOLD_QUANTITY * 100 * ureg("m2")).to("W").magnitude

TEST_RMI = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        # directly conditioned zone
                        {
                            "id": "hvac_1_1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 100,
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 1-1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_1",
                                }
                            ],
                        },
                    ],
                },
                {
                    "id": "Building Segment 2",
                    "heating_ventilating_air_conditioning_systems": [
                        # directly conditioned zone
                        {
                            "id": "hvac_2_1",
                            "cooling_system": {
                                "id": "csys_2_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "floor_area": 200,
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 2-1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2_1",
                                }
                            ],
                        },
                    ],
                },
                {
                    "id": "Building Segment 3",
                    "zones": [
                        {
                            "id": "Thermal Zone 3",
                            "volume": 100,
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 200,
                                    "lighting_space_type": "LOBBY_HOTEL",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_1_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_2",  # semi-heated
                                    "area": 10,  # m2
                                    "tilt": 90,  # wall
                                    "construction": {
                                        "id": "construction_1",
                                        "u_factor": 1.2,
                                    },
                                }
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}


TEST_RMD_FULL = {"id": "229", "ruleset_model_descriptions": [TEST_RMI]}

TEST_RMI_UNIT = quantify_rmr(TEST_RMD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_predominant_hvac_building_area_type__residential():
    test_rmi_unit_residential = deepcopy(TEST_RMI_UNIT)
    test_rmi_unit_residential["buildings"][0]["building_segments"][1][
        "lighting_building_area_type"
    ] = "MULTIFAMILY"
    assert (
        get_predominant_hvac_building_area_type("CZ4A", test_rmi_unit_residential)
        == "RESIDENTIAL"
    )