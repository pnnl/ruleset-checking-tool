import pydash
from rct229.schema.schema_enums import SchemaEnums

HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7

DAY_OF_WEEK = SchemaEnums.schema_enums["DayOfWeekOptions"]

DATE_NUMBER_MAP = {
    DAY_OF_WEEK.MONDAY: 0,
    DAY_OF_WEEK.TUESDAY: 1,
    DAY_OF_WEEK.WEDNESDAY: 2,
    DAY_OF_WEEK.THURSDAY: 3,
    DAY_OF_WEEK.FRIDAY: 4,
    DAY_OF_WEEK.SATURDAY: 5,
    DAY_OF_WEEK.SUNDAY: 6,
}


def get_most_used_weekday_hourly_schedule(
    hourly_data: list, day_of_week_for_jan_first: str
) -> list[float | int]:
    """
    Get the most used weekday hourly schedule from an annual 8760/8784 schedule as list of hourly values for a 24
    hour period.

    Parameters
    ----------
    hourly_data: list of data - hourly values
    day_of_week_for_jan_first: schema day of week option

    Returns
    -------
    most_used_schedule: list contains 24 hours data.
    """
    assert (
        len(hourly_data) == 8760 or len(hourly_data) == 8784
    ), f"Insufficient data, expected 8760 or 8784 hours data, but got {len(hourly_data)} instead."
    # verified this is 8760 or 8784 (leap year) hours
    number_of_days = int(len(hourly_data) / HOURS_IN_DAY)
    daily_data = pydash.chunk(hourly_data, HOURS_IN_DAY)
    days_of_week = [
        (i + DATE_NUMBER_MAP[day_of_week_for_jan_first]) % DAYS_IN_WEEK
        for i in range(number_of_days)
    ]
    # 5 (saturday)
    weekdays_data = [day for i, day in enumerate(daily_data) if days_of_week[i] < 5]
    # Calculate the frequency of each 24-hour schedule
    schedule_frequencies = [tuple(day) for day in weekdays_data]
    schedule_counts = pydash.count_by(schedule_frequencies)

    return list(max(schedule_counts, key=schedule_counts.get))
