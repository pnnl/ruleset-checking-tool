from unittest.mock import patch

import pytest

from rct229.ruleset_functions.get_building_scc_window_wall_ratios_dict import (
    get_building_scc_window_wall_ratios_dict,
)
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import schema_validate_rmr

CLIMATE_ZONE = "CZ0A"


TEST_RMR = {
    "id": "test_rmr",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                {
                    "id": "bldg_seg_1",
                    "zones": [
                        {
                            "id": "zone_1_1",
                            "surfaces": [
                                # Mock for SCC.EXTERIOR_RESIDENTIAL and OST.ABOVE_GRADE_WALL
                                {
                                    "id": "surface_1_1_1",
                                    "area": 16,  # m2
                                    "subsurfaces": [
                                        # DOOR with not (glazed_area > opaque_area)
                                        # window_area = 0
                                        {
                                            "id": "subsurface_1_1_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                        },
                                        # DOOR with (glazed_area > opaque_area)
                                        # window_area = 4
                                        {
                                            "id": "subsurface_1_1_1_2",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                        },
                                        # Not a DOOR
                                        # window_area = 4
                                        {
                                            "id": "subsurface_1_1_1_3",
                                            "classification": "OTHER",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                        },
                                    ],
                                },
                                # Mock for SCC.EXTERIOR_NON_RESIDENTIAL and OST.ABOVE_GRADE_WALL
                                {
                                    "id": "surface_1_1_2",
                                    "area": 12,  # m2
                                    "subsurfaces": [
                                        # Not a DOOR
                                        # window_area = 3
                                        {
                                            "id": "subsurface_1_1_2_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 3,
                                        },
                                    ],
                                },
                                # Mock for SCC.EXTERIOR_MIXED and OST.ABOVE_GRADE_WALL
                                {
                                    "id": "surface_1_1_3",
                                    "area": 12,  # m2
                                    "subsurfaces": [
                                        # Not a DOOR
                                        # window_area = 3
                                        {
                                            "id": "subsurface_1_1_3_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 3,
                                        },
                                    ],
                                },
                                # Mock for SCC.SEMI_EXTERIOR and OST.ABOVE_GRADE_WALL
                                {
                                    "id": "surface_1_1_4",
                                    "area": 12,  # m2
                                    "subsurfaces": [
                                        # Not a DOOR
                                        # window_area = 3
                                        {
                                            "id": "subsurface_1_1_4_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 3,
                                        },
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                    ],
                }
            ],
        }
    ],
}

TEST_SCC_DICT = {
    "surface_1_1_1": SCC.EXTERIOR_RESIDENTIAL,
    "surface_1_1_2": SCC.EXTERIOR_NON_RESIDENTIAL,
    "surface_1_1_3": SCC.EXTERIOR_MIXED,
    "surface_1_1_4": SCC.SEMI_EXTERIOR,
}

TEST_RMR_12 = {"id": "229_01", "ruleset_model_instances": [TEST_RMR]}

TEST_BUILDING = quantify_rmr(TEST_RMR_12)["ruleset_model_instances"][0]["buildings"][0]


def test__TEST_RMR__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMR_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


@patch(
    "rct229.ruleset_functions.get_building_scc_window_wall_ratios_dict.get_opaque_surface_type",
    return_value=OST.ABOVE_GRADE_WALL,
)
@patch(
    "rct229.ruleset_functions.get_building_scc_window_wall_ratios_dict.get_surface_conditioning_category_dict",
    return_value=TEST_SCC_DICT,
)
def test__get_building_scc_skylight_roof_ratios_dict(
    mock_get_surface_conditioning_category_dict, mock_get_opaque_surface_type
):
    assert get_building_scc_window_wall_ratios_dict(CLIMATE_ZONE, TEST_BUILDING) == {
        SCC.EXTERIOR_RESIDENTIAL: 0.5,
        SCC.EXTERIOR_NON_RESIDENTIAL: 0.25,
        SCC.EXTERIOR_MIXED: 0.25,
        SCC.SEMI_EXTERIOR: 0.25,
    }
