from unittest.mock import patch

from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_scc_window_wall_ratios_dict import (
    get_building_scc_window_wall_ratios_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

CLIMATE_ZONE = "CZ0A"


TEST_RMD = {
    "id": "test_rmd",
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
                                    "tilt": 90,  # degrees
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
                                    "tilt": 90,  # degrees
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
                                    "tilt": 90,  # degrees
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
                                    "tilt": 90,  # degrees
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
                                # Mock for SCC.UNREGULATED and OST.ABOVE_GRADE_WALL
                                {
                                    "id": "surface_1_1_5",
                                    "area": 100,  # m2
                                    "tilt": 90,  # degrees
                                },
                                # Mock for SCC.UNREGULATED and OST.ROOF
                                {
                                    "id": "surface_1_1_6",
                                    "area": 100,  # m2
                                    "tilt": 0,  # degrees
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
    "type": "BASELINE_0",
}

TEST_SCC_DICT = {
    "surface_1_1_1": SCC.EXTERIOR_RESIDENTIAL,
    "surface_1_1_2": SCC.EXTERIOR_NON_RESIDENTIAL,
    "surface_1_1_3": SCC.EXTERIOR_MIXED,
    "surface_1_1_4": SCC.SEMI_EXTERIOR,
    "surface_1_1_5": SCC.UNREGULATED,
    "surface_1_1_6": SCC.UNREGULATED,
}

TEST_RMD_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_BUILDING = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0]["buildings"][
    0
]
TEST_CONSTRUCTIONS = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0].get(
    "constructions"
)


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


@patch(
    "rct229.rulesets.ashrae9012019.ruleset_functions.get_building_scc_window_wall_ratios_dict.get_surface_conditioning_category_dict",
    return_value=TEST_SCC_DICT,
)
def test__get_building_scc_skylight_roof_ratios_dict(mock_get_opaque_surface_type):
    assert get_building_scc_window_wall_ratios_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING
    ) == {
        SCC.EXTERIOR_RESIDENTIAL: 0.5,
        SCC.EXTERIOR_NON_RESIDENTIAL: 0.25,
        SCC.EXTERIOR_MIXED: 0.25,
        SCC.SEMI_EXTERIOR: 0.25,
    }
