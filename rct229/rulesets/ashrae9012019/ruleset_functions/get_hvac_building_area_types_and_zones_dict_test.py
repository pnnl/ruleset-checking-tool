from copy import deepcopy

from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

TEST_RMI = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
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
                        },
                    ],
                },
                {
                    "id": "Building Segment 2",
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
                        },
                    ],
                },
            ],
        },
    ],
}


TEST_RMD_FULL = {"id": "229", "ruleset_model_instances": [TEST_RMI]}

TEST_RMI_UNIT = quantify_rmr(TEST_RMD_FULL)["ruleset_model_instances"][0]


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_hvac_building_area_types_and_zones_dict__undetermined_predominante_success():
    assert get_hvac_building_area_types_and_zones_dict(TEST_RMI_UNIT) == {
        "OTHER_NON_RESIDENTIAL": {
            "zone_ids": ["Thermal Zone 2", "Thermal Zone 1"],
            "floor_area": 300 * ureg("m2").to("ft2"),
        }
    }


def test__get_hvac_building_area_types_and_zones_dict__residential_predominate_success():
    test_rmi_unit_residential = deepcopy(TEST_RMI_UNIT)
    test_rmi_unit_residential["buildings"][0]["building_segments"][1][
        "lighting_building_area_type"
    ] = "MULTIFAMILY"
    assert get_hvac_building_area_types_and_zones_dict(test_rmi_unit_residential) == {
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
    test_rmi_unit_residential = deepcopy(TEST_RMI_UNIT)
    test_rmi_unit_residential["buildings"][0]["building_segments"][1][
        "lighting_building_area_type"
    ] = "RELIGIOUS_FACILITY"
    assert get_hvac_building_area_types_and_zones_dict(test_rmi_unit_residential) == {
        "PUBLIC_ASSEMBLY": {
            "zone_ids": ["Thermal Zone 1", "Thermal Zone 2"],
            "floor_area": 300 * ureg("m2").to("ft2"),
        }
    }
