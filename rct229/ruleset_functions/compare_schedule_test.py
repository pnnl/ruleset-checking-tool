import pytest

from rct229.ruleset_functions.compare_schedules import compare_schedules
from rct229.utils.assertions import RCTFailureException


def test__Test_Schedule_Compare_Success_1():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8760 compared and match with eflh difference = 1.0
    """
    schedule_1 = [0.8] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [2] * 8760
    multiplier = 0.8
    results = compare_schedules(
        schedule_1, schedule_2, mask_schedule, multiplier, False
    )
    assert (
        results["total_hours_compared"] == 8760.0
        and results["total_hours_match"] == 8760.0
        and results["eflh_difference"] == 0
    )


def test__Test_Schedule_Compare_Success_2():
    """
    Test that will not apply multiplier to schedule_2 to match schedule_1.
    Expect 8760 compared and match with eflh difference = 1.0
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [1.0] * 8760
    multiplier = 0.8
    results = compare_schedules(
        schedule_1, schedule_2, mask_schedule, multiplier, False
    )
    assert (
        results["total_hours_compared"] == 8760.0
        and results["total_hours_match"] == 8760.0
        and results["eflh_difference"] == 0
    )


def test__Test_Schedule_Compare_Success_3():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8760 compared but 0 match with eflh difference = 1.25
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [2.0] * 8760
    multiplier = 0.8
    results = compare_schedules(
        schedule_1, schedule_2, mask_schedule, multiplier, False
    )
    assert (
        results["total_hours_compared"] == 8760.0
        and results["total_hours_match"] == 0.0
        and abs(results["eflh_difference"] - (8760 - 8760*0.8)) <= 0.001
    )


def test__Test_Schedule_Compare_Success_4():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8784 compared and 8784 match with eflh difference = 1.0

    """
    schedule_1 = [1.0] * 8784
    schedule_2 = [1.0] * 8784
    mask_schedule = [1.0] * 8784
    multiplier = 0.8
    results = compare_schedules(schedule_1, schedule_2, mask_schedule, multiplier, True)
    assert (
        results["total_hours_compared"] == 8784.0
        and results["total_hours_match"] == 8784.0
        and results["eflh_difference"] == 0
    )


def test__Test_Schedule_Compare_Failed_1():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    Expect 8784 compared and 8784 match with eflh difference = 1.0,
    but the actual length of schedule is 8760, raise exception
    """
    schedule_1 = [1.0] * 8760
    schedule_2 = [1.0] * 8760
    mask_schedule = [2.0] * 8760
    multiplier = 0.8
    try:
        results = compare_schedules(
            schedule_1, schedule_2, mask_schedule, multiplier, True
        )
    except RCTFailureException as rfe:
        assert str(rfe) == (
            "Failed when comparing hourly schedules with target number of hours. target "
            "number of hour: 8784, number of hours of schedule_1 : 8760; number of hours "
            "of schedule_2: 8760; number of hours of mask_schedule: 8760"
        )


def test__Test_Schedule_Compare_Failed_2():
    """
    Test that will apply multiplier to schedule_2 to match schedule_1.
    schedule_2 has 8784 hours and schedule 1 has 8760 hours - mismached, raise exception
    """
    schedule_1 = [1.0] * 8784
    schedule_2 = [1.0] * 8784
    mask_schedule = [2.0] * 8784
    multiplier = 0.8
    try:
        results = compare_schedules(
            schedule_1, schedule_2, mask_schedule, multiplier, True
        )
    except RCTFailureException as rfe:
        assert str(rfe) == (
            "Failed when comparing hourly schedules with target number of hours. target "
            "number of hour: 8784, number of hours of schedule_1 : 8760; number of hours "
            "of schedule_2: 8784; number of hours of mask_schedule: 8760"
        )
