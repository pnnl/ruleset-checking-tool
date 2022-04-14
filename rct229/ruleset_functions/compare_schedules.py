from rct229.utils.assertions import RCTFailureException

REGULAR_YEAR_HOUR = 8760
LEAP_YEAR_HOUR = 8784


def compare_schedules(schedule_1: list, schedule_2: list, mask_schedule: list, comparison_factor: float, is_leap_year: bool):
    """compare two schedules and determine if they match with or without a comparison factor when applicable
        NOTE: The function only works with hourly schedule for now.

        Parameters
        ----------
        schedule_1: list, First schedule [0.187, 0.187, 0.187, ... ]
        schedule_2: list, Second schedule [0.187, 0.187, 0.187, ...]
        mask_schedule: list, The schedule that defines comparison mode for all hours (8760 or 8784) in a year, i.e.
            if hourly value is 1, schedule_1 is evaluated to be equal to schedule_2;
            if hourly value is 2, schedule_1 is evaluated to be equal to schedule_2 times the comparison factor;
            if hourly value is 0, comparison was skipped for that particular hour
            (example when evaluating shut off controls, only he building closed hrs are evaluated) [1,1,1,1,1...]
        comparison_factor: float, The target multiplier number for schedule_1 compared to schedule_2, i.e. when applicable,
            the hourly value in schedule_1 shall be equal to that in schedule_2 times the comparison_factor. 1.0
        is_leap_year: bool, indicate whether the comparison is in a leap year or not. True / False

        Returns
        -------
        A dictionary containing the total number of hours that the function compares,
        the number of hours schedule_1 matches schedule_2 with the comparison_factor,
        EFLH difference for schedule_1 and schedule_2,
        i.e. {
            "TOTAL_HOURS_COMPARED": total_hours_compared,
            "TOTAL_HOURS_MATCH": total_hours_match,
            "EFLH_DIFFERENCE: EFLH_difference
            }
        """
    num_hours = REGULAR_YEAR_HOUR
    if is_leap_year:
        num_hours = LEAP_YEAR_HOUR

    if len(schedule_1) != len(schedule_2) or len(schedule_1) != len(mask_schedule) or len(schedule_1) != num_hours:
        raise RCTFailureException(f"Failed when comparing hourly schedules with target number of hours. target number of hour: {num_hours}, "
                                  f"number of hours of schedule_1 : {len(schedule_1)}; "
                                  f"number of hours of schedule_2: {len(schedule_2)}; "
                                  f"number of hours of mask_schedule: {len(mask_schedule)}")

    total_hours_compared = 0.0
    eflh_schedule_1 = 0.0
    eflh_schedule_2 = 0.0
    total_hours_match = 0.0
    for index, hourly_value in enumerate(mask_schedule):
        total_hours_compared += 1
        if hourly_value == 1:
            eflh_schedule_1 += schedule_1[index]
            eflh_schedule_2 += schedule_2[index]
            if schedule_1[index] == schedule_2[index]:
                total_hours_match += 1
        elif hourly_value == 2:
            eflh_schedule_1 += schedule_1[index]
            eflh_schedule_2 += schedule_2[index] * comparison_factor
            if schedule_1[index] == schedule_2[index] * comparison_factor:
                total_hours_match += 1
    eflh_difference = eflh_schedule_1 / eflh_schedule_2

    return {
        "total_hours_compared": total_hours_compared,
        "total_hours_match": total_hours_match,
        "eflh_difference": eflh_difference
    }

