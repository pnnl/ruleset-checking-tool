from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.utils.assertions import RCTFailureException


def test__compare_schedules__identical_compare_all_hours():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8760 compared and match with eflh difference = 0.0
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [1] * 8760
    results = compare_schedules(schedule_1, schedule_2, mask_schedule)
    assert (
        results["total_hours_compared"] == 8760.0
        and results["total_hours_matched"] == 8760.0
        and results["eflh_difference"] == 0.0
    )


def test__compare_schedules__identical_compare_no_hours():
    """
    Test that will not compare any hours between two schedules.
    Expect 0.0 compared and match with eflh difference = 0.0
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [0.0] * 8760
    results = compare_schedules(schedule_1, schedule_2, mask_schedule)
    assert (
        results["total_hours_compared"] == 0.0
        and results["total_hours_matched"] == 0.0
        and results["eflh_difference"] == 0.0
    )


def test__compare_schedules__not_identical_compare_all_hours():
    """
    Test when two schedules are not identical.
    Expect 8760.0 compared and match with eflh difference = 100.0
    """
    schedule_1 = [1.0] * 8760
    # `schedule_2` has different schedules with `schedule_1` for the first 100 hrs to test out the `if schedule_1[index] == schedule_2[index]:` logic
    schedule_2 = [0.0] * 100 + [1.0] * 8660
    mask_schedule = [1] * 8760
    results = compare_schedules(schedule_1, schedule_2, mask_schedule)
    assert (
        results["total_hours_compared"] == 8760.0
        and results["total_hours_matched"] == 8660.0
        and results["eflh_difference"] == 100.0
    )


def test__compare_schedules__identical_compare_all_hours_leap_year():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8784 compared and 8784 match with eflh difference = 1.0,
    but the actual length of schedule is 8760, raise exception
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [1.0] * 8760
    try:
        results = compare_schedules(schedule_1, schedule_2, mask_schedule)
    except RCTFailureException as rfe:
        assert str(rfe) == (
            "Failed when comparing hourly schedules with target number of hours. target "
            "number of hour: 8784, number of hours of schedule_1 : 8760; number of hours "
            "of schedule_2: 8760; number of hours of mask_schedule: 8760"
        )
