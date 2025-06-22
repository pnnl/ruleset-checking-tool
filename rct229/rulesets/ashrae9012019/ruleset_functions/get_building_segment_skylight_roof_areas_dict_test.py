from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CRAWLSPACE_HEIGHT_THRESHOLD as CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

CLIMATE_ZONE = "CZ0A"
POWER_DELTA = 1
SYSTEM_MIN_HEATING_OUTPUT_QUANTITY = table_3_2_lookup(CLIMATE_ZONE)[
    "system_min_heating_output"
]

# Convert pint quantities to match schema units
SYSTEM_MIN_HEATING_OUTPUT = (
    (SYSTEM_MIN_HEATING_OUTPUT_QUANTITY * 100 * ureg("m2")).to("W").magnitude
)
CRAWLSPACE_HEIGHT_THRESHOLD = CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY.to("m").magnitude


# This single RMD is intended to exercise all the get_zone_conditioning_category_dict() code
TEST_RMD = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 3.2366105565544463,
        }
    ],
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # area_type_vertical_fenestration is nonresidential type
                # In total this building segment has 10m2 windows and 20m2 walls.
                {
                    "id": "bldg_seg_1",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_vertical_fenestration": "HOTEL_MOTEL_SMALL",
                    "heating_ventilating_air_conditioning_systems": [
                        # Used for zone_1_2, directly conditioned zone
                        {
                            "id": "hvac_1_2",
                            "heating_system": {
                                "id": "hsys_1_2_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_1_2 => directly_conditioned_zone
                        # zone has no residential spaces but a space has a lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # Not zone_has_residential_spaces and zone_has_nonesidential_spaces
                        #  => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        {
                            "id": "zone_1_2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_1",
                                    "area": 10,  # m2
                                    "tilt": 10,  # roof
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # wall surface to verify the roof type check condition for branch coverage
                                {
                                    "id": "surface_1_2_2",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_1",
                                    "area": 10,  # m2
                                    "tilt": 90,  # wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_2_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_2",
                                }
                            ],
                        },
                        # below zone is a `UNCONDITIONED` zone for verifying zone type condition for branch coverage
                        {
                            "id": "zone_1_3",
                            "volume": 300,  # m3
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_3_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_1",
                                    "area": 10,  # m2
                                    "tilt": 90,  # wall
                                    "construction": "construction_1",
                                }
                            ],
                        },
                    ],
                },
            ],
        }
    ],
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 3.2366105565544463,
        }
    ],
    "type": "BASELINE_0",
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


def test__get_building_segment_skylight_roof_areas_dict():
    assert get_building_segment_skylight_roof_areas_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING
    ) == {
        "bldg_seg_1": {
            "total_envelope_roof_area": 10 * ureg("m2"),
            "total_skylight_area": 5 * ureg("m2"),
        }
    }
