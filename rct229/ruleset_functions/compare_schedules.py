
def compare_schedules(schedule_1, schedule_2, mask_schedule, comparison_factor, is_leap_year):
    """compare two schedules and determine if they match with or without a comparison factor when applicable
        NOTE: The function only works with hourly schedule for now.

        Parameters
        ----------
        schedule_1: First schedule
        schedule_2: Second schedule
        mask_schedule: The schedule that defines comparison mode for all hours (8760 or 8784) in a year, i.e. if hourly value is 1, schedule_1 is evaluated to be equal to schedule_2; if hourly value is 2, schedule_1 is evaluated to be equal to schedule_2 times the comparison factor; if hourly value is 0, comparison was skipped for that particular hour (example when evaluating shut off controls, only he building closed hrs are evaluated).
        comparison_factor: The target multiplier number for schedule_1 compared to schedule_2, i.e. when applicable, the hourly value in schedule_1 shall be equal to that in schedule_2 times the comparison_factor.
        is_leap_year: boolean, indicate whether the comparison is in a leap year or not.

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