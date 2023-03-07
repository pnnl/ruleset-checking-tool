import datetime
from collections import Counter

from rct229.rule_engine.rulesets import LeapYear
from rct229.utils.assertions import RCTFailureException, assert_

HOURS_IN_DAY = 24
NUM_DAYS_WEEKDAYS = 5


def get_most_used_weekday_hourly_schedule(hourly_data: list, year: int):
    """
    Get the most used weekday hourly schedule from an annual 8760/8784 schedule as list of hourly values for a 24
    hour period.

    Parameters
    ----------
    hourly_data: list of data - hourly values
    year: int, years, need to be four digits

    Returns
    -------
    most_used_schedule: list contains 24 hours data.
    """
    # validate the year argument - might need to add a smaller range for the year
    if not isinstance(year, int) or year < 1 or year > 9999:
        raise RCTFailureException(
            f"Invalid year {year}. Year needs to be an integer, greater than 1 and smaller than 9999"
        )

    # check if the year is a leap year - perfectly divisible by four -
    # but not 100, unless it's divisible by 400
    is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    # Verify the list has the correct number of hours for the year type
    assert_(
        (is_leap_year and len(hourly_data) == LeapYear.LEAP_YEAR_HOURS)
        or (not is_leap_year and len(hourly_data) == LeapYear.REGULAR_YEAR_HOURS),
        f"The number of hours does not match to the year. Year: {year}, number of hours: {len(hourly_data)}",
    )

    # create a datetime object for the first hour of the year
    start_datetime = datetime.datetime(year, 1, 1, 0)

    # create a list to store the 24-hour schedules for each day of the week
    schedules_by_day_of_week = [[] for _ in range(NUM_DAYS_WEEKDAYS)]

    # loop over each hour in the year
    for i in range(0, len(hourly_data), HOURS_IN_DAY):
        # calculate the datetime for the current hour
        current_datetime = start_datetime + datetime.timedelta(hours=i)
        # get the weekday (Monday is 0, Friday is 4)
        weekday = current_datetime.weekday()
        # We only need weekdays, excluding weekends
        if weekday < NUM_DAYS_WEEKDAYS:
            # get the 24-hour schedule for the current day
            day_schedule = tuple(hourly_data[i : i + HOURS_IN_DAY])
            schedules_by_day_of_week[weekday].append(day_schedule)

    # create a Counter object to count the occurrences of each 24-hour schedule
    schedule_counts = Counter(
        schedule for schedules in schedules_by_day_of_week for schedule in schedules
    )
    most_common_schedule, count = schedule_counts.most_common(1)[0]
    return list(most_common_schedule)
