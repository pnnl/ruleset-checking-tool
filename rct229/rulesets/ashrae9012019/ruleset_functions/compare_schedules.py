from typing import TypedDict, List

from rct229.rule_engine.rulesets import LeapYear
from rct229.utils.assertions import assert_


class CompareSchedulesEFLHDifference(TypedDict):
    total_hours_compared: int
    total_hours_matched: int
    eflh_difference: float


def compare_schedules(
    schedule_1: list[float],
    schedule_2: list[float],
    mask_schedule: list[float],
) -> CompareSchedulesEFLHDifference:
    """Compare two schedules and determine if they match with or without a comparison factor when applicable
    NOTE: The function only works with hourly schedule for now.

    Parameters
    ----------
    schedule_1: List[float], example: [0.187, 0.187, 0.187, ... ]
    schedule_2: List[float], example: [0.1, 0.1, 0.1, ... ]
    mask_schedule: List[float], The schedule that defines comparison mode for all hours (8760 or 8784) in a year, i.e.
        if hourly value is 1, schedule_1 is evaluated to be equal to schedule_2;
        if hourly value is 2, schedule_1 is evaluated to be equal to schedule_2 times the comparison factor;
        if hourly value is 0, comparison was skipped for that particular hour
        (example when evaluating shut off controls, only the building closed hrs are evaluated) example: [1,1,1,1,1...]

    Returns
    -------
    A dictionary containing the total number of hours that the function compares,
    the number of hours schedule_1 matches schedule_2 with the comparison_factor,
    EFLH difference for schedule_1 and schedule_2,
    i.e. {
        "total_hours_compared": total_hours_compared,
        "total_hours_matched": total_hours_match,
        "eflh_difference: EFLH_difference
        }
    """

    assert_(
        (len(schedule_1) == len(schedule_2) and len(schedule_1) == len(mask_schedule)),
        f"Failed when comparing hourly schedules. number of hours of schedule_1 : {len(schedule_1)}; number of hours of schedule_2: {len(schedule_2)}; number of hours of mask_schedule: {len(mask_schedule)}",
    )

    total_hours_compared = 0
    eflh_schedule_1 = 0.0
    eflh_schedule_2 = 0.0
    total_hours_matched = 0
    for index, hourly_value in enumerate(mask_schedule):
        if hourly_value == 1:
            total_hours_compared += 1
            eflh_schedule_1 += schedule_1[index]
            eflh_schedule_2 += schedule_2[index]
            if schedule_1[index] == schedule_2[index]:
                total_hours_matched += 1

    eflh_difference = eflh_schedule_1 - eflh_schedule_2

    return {
        "total_hours_compared": total_hours_compared,
        "total_hours_matched": total_hours_matched,
        "eflh_difference": eflh_difference,
    }
