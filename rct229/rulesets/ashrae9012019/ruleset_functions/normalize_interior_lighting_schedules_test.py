from rct229.rulesets.ashrae9012019.ruleset_functions.normalize_interior_lighting_schedules import (
    normalize_interior_lighting_schedules,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "building_1",
    "buildings": [
        {
            "id": "building 1",
            "building_segments": [
                {
                    "id": "building_segment 1",
                    "zones": [
                        {
                            "id": "zone_1",
                            "spaces": [
                                {
                                    "id": "space_1",
                                    "occupant_multiplier_schedule": "Required Occupancy Sched 1",
                                    "lighting_space_type": "OFFICE_ENCLOSED",
                                    "interior_lighting": [
                                        {
                                            "id": "light_1",
                                            "power_per_area": 2.3,
                                            "lighting_multiplier_schedule": "light_multiplier_sched_1",
                                            "occupancy_control_type": "MANUAL_ON",
                                            # control credit: 0.375
                                            "are_schedules_used_for_modeling_occupancy_control": True,
                                        },
                                        {
                                            "id": "light_2",
                                            "power_per_area": 5.5,
                                            "lighting_multiplier_schedule": "light_multiplier_sched_1",
                                            "occupancy_control_type": "FULL_AUTO_ON",
                                            # control credit: 0.3
                                            "are_schedules_used_for_modeling_occupancy_control": True,
                                        },
                                        {
                                            "id": "light_2",
                                            "power_per_area": 2.3,
                                            "lighting_multiplier_schedule": "light_multiplier_sched_1",
                                            "occupancy_control_type": "NONE",
                                            # control credit: 0.0
                                            "are_schedules_used_for_modeling_occupancy_control": False,
                                        },
                                        {
                                            "id": "light_3",
                                            "power_per_area": 4.0,
                                            "lighting_multiplier_schedule": "light_multiplier_sched_1",
                                            "occupancy_control_type": "NONE",
                                            # control credit: 0.0
                                            "are_schedules_used_for_modeling_occupancy_control": True,
                                        },
                                    ],
                                    "floor_area": 23.25,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_SPACE_RMD = {
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

TEST_SCHEDULES = {
    "schedules": [{"id": "light_multiplier_sched_1", "hourly_values": [0.8] * 8760}]
}

ZONE_HEIGHT = 10.0
TEST_SPACES = quantify_rmd(TEST_SPACE_RMD)["ruleset_model_descriptions"][0][
    "buildings"
][0]["building_segments"][0]["zones"][0]["spaces"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_SPACE_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__normalize_space_schedules__success_1():
    """
    Test to test three sets of interior lighting in a space
    the total power per area is: 2.3 + 5.5 + 2.3 + 4.0
    light_1, 2.3 W/m2, MANUAL_ON => control credit: 0.375,
    light_2, 5.5 W/m2, FULL_AUTO_ON => control credit: 0.3,
    light_3. 2.3 W/m2, No control => control credit: 0.0,
    light_4. 4.0 W/m2, No control => control credit: 0.0
    hourly value 0.8
    """

    test_space_normalized_schedule_array = [
        (
            0.8
            * (
                1 / (1 - 0.375) * 2.3
                + 1 / (1 - 0.3) * 5.5
                + 1 / (1 - 0.0) * 2.3
                + 1 / (1 - 0.0) * 4.0
            )
        )
        / (2.3 + 5.5 + 2.3 + 4.0)
    ] * 8760

    results = normalize_interior_lighting_schedules(
        space=TEST_SPACES,
        space_height=ZONE_HEIGHT,
        schedules=TEST_SCHEDULES["schedules"],
    )
    assert test_space_normalized_schedule_array == results
