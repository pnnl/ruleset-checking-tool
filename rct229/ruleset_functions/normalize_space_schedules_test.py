import pytest

from rct229.ruleset_functions.normalize_space_schedules import normalize_space_schedules

TEST_SPACES = {
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
                    "are_schedules_used_for_modeling_occupancy_control": True
                },
                {
                    "id": "light_2",
                    "power_per_area": 5.5,
                    "lighting_multiplier_schedule": "light_multiplier_sched_1",
                    "occupancy_control_type": "FULL_AUTO_ON",
                    # control credit: 0.3
                    "are_schedules_used_for_modeling_occupancy_control": True
                },
                {
                    "id": "light_2",
                    "power_per_area": 2.3,
                    "lighting_multiplier_schedule": "light_multiplier_sched_1",
                    "occupancy_control_type": "NONE",
                    # control credit: 0.0
                    "are_schedules_used_for_modeling_occupancy_control": False
                }
            ],
            "floor_area": 23.25
        }
    ]
}

TEST_SCHEDULES = {
    "schedules": [
        {
            "id": "light_multiplier_sched_1",
            "hourly_values": [0.8] * 8760
        }
    ]
}

ZONE_HEIGHT = 10.0


def test__normalize_space_schedules_success_1():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8760 compared and match with eflh difference = 1.0
    """

    test_space_normalized_schedule_array = [(0.8 * (1 / (1-0.375) * 2.3 + 1 / (1-0.3) * 5.5 + 1 / (1-0.0) * 2.3)) / (2.3+5.5+2.3)] * 8760

    results = normalize_space_schedules(
        space=TEST_SPACES["spaces"][0], zone_height=ZONE_HEIGHT, schedules=TEST_SCHEDULES
    )
    assert (
        test_space_normalized_schedule_array == results
    )