from copy import deepcopy

from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

POWER_DELTA = 1
POWER_THRESHOLD_100 = (CAPACITY_THRESHOLD_QUANTITY * 100 * ureg("m2")).to("W").magnitude

TEST_RMD = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 1.2,
        }
    ],
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
                                    "construction": "construction_1",
                                }
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 1.2,
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


def test__get_hvac_building_area_types_and_zones_dict__undetermined_predominante_success():
    assert get_hvac_building_area_types_and_zones_dict("CZ4A", TEST_RMD_UNIT) == {
        "OTHER_NON_RESIDENTIAL": {
            "zone_ids": ["Thermal Zone 2", "Thermal Zone 1"],
            "floor_area": 300 * ureg("m2").to("ft2"),
        }
    }


def test__get_hvac_building_area_types_and_zones_dict__residential_predominate_success():
    test_rmd_unit_residential = deepcopy(TEST_RMD_UNIT)
    test_rmd_unit_residential["buildings"][0]["building_segments"][1][
        "lighting_building_area_type"
    ] = "MULTIFAMILY"
    assert get_hvac_building_area_types_and_zones_dict(
        "CZ4A", test_rmd_unit_residential
    ) == {
        "RESIDENTIAL": {
            "zone_ids": ["Thermal Zone 2"],
            "floor_area": 200 * ureg("m2").to("ft2"),
        },
        "OTHER_NON_RESIDENTIAL": {
            "zone_ids": ["Thermal Zone 1"],
            "floor_area": 100 * ureg("m2").to("ft2"),
        },
    }


def test__get_hvac_building_area_types_and_zones_dict__public_assembly_predominate_success():
    test_rmd_unit_residential = deepcopy(TEST_RMD_UNIT)
    test_rmd_unit_residential["buildings"][0]["building_segments"][1][
        "lighting_building_area_type"
    ] = "RELIGIOUS_FACILITY"
    assert get_hvac_building_area_types_and_zones_dict(
        "CZ4A", test_rmd_unit_residential
    ) == {
        "PUBLIC_ASSEMBLY": {
            "zone_ids": ["Thermal Zone 1", "Thermal Zone 2"],
            "floor_area": 300 * ureg("m2").to("ft2"),
        }
    }
