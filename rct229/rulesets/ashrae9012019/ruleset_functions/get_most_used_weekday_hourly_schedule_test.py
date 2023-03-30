import datetime

from rct229.rulesets.ashrae9012019.ruleset_functions.get_most_used_weekday_hourly_schedule import (
    get_most_used_weekday_hourly_schedule,
)


def test__get_most_used_weekday_hourly_schedule__success_1():
    year = 2015
    week = [
        [0.8] * 24,  # monday
        [0.8] * 24,  # tuesday
        [0.8] * 24,  # wednesday
        [0.8] * 24,  # thursday
        [0.9] * 24,  # friday
        [0.9] * 24,  # saturday
        [0.9] * 24,  # sunday
    ]
    hourly_value = [0] * 8760
    start_datetime = datetime.datetime(year, 1, 1, 0)
    for i in range(8760):
        current_datetime = start_datetime + datetime.timedelta(hours=i)
        weekday = current_datetime.weekday()
        hour = current_datetime.hour
        hourly_value[i] = week[weekday][hour]
    most_used_schedule = get_most_used_weekday_hourly_schedule(hourly_value, "THURSDAY")
    assert most_used_schedule == [0.8] * 24


def test__get_most_used_weekday_hourly_schedule__success_2():
    """
    In this case, the [0.8] shall still win because we are only counting weekdays
    Returns
    -------

    """
    year = 2015
    week = [
        [0.8] * 24,  # monday
        [0.8] * 24,  # tuesday
        [0.8] * 24,  # wednesday
        [0.9] * 24,  # thursday
        [0.9] * 24,  # friday
        [0.9] * 24,  # saturday
        [0.9] * 24,  # sunday
    ]
    hourly_value = [0] * 8760
    start_datetime = datetime.datetime(year, 1, 1, 0)
    for i in range(8760):
        current_datetime = start_datetime + datetime.timedelta(hours=i)
        weekday = current_datetime.weekday()
        hour = current_datetime.hour
        hourly_value[i] = week[weekday][hour]
    most_used_schedule = get_most_used_weekday_hourly_schedule(hourly_value, "THURSDAY")
    assert most_used_schedule == [0.8] * 24


def test__get_most_used_weekday_hourly_schedule__success_3():
    """
    In this case, the [0.9] shall win because there three of them
    Returns
    -------

    """
    year = 2015
    week = [
        [0.8] * 24,  # monday
        [0.8] * 24,  # tuesday
        [0.9] * 24,  # wednesday
        [0.9] * 24,  # thursday
        [0.9] * 24,  # friday
        [0.9] * 24,  # saturday
        [0.9] * 24,  # sunday
    ]
    hourly_value = [0] * 8760
    start_datetime = datetime.datetime(year, 1, 1, 0)
    for i in range(8760):
        current_datetime = start_datetime + datetime.timedelta(hours=i)
        weekday = current_datetime.weekday()
        hour = current_datetime.hour
        hourly_value[i] = week[weekday][hour]
    most_used_schedule = get_most_used_weekday_hourly_schedule(hourly_value, "THURSDAY")
    assert most_used_schedule == [0.9] * 24


def test__get_most_used_weekday_hourly_schedule__no_repeated_4():
    """
    In this case, the [0.4] shall win because there are 53 Thursday in 2015
    -------

    """
    year = 2015
    week = [
        [0.1] * 24,  # monday 52 in year 2015
        [0.2] * 24,  # tuesday 52 in year 2015
        [0.3] * 24,  # wednesday 52 in year 2015
        [0.4] * 24,  # thursday 53 in year 2015
        [0.5] * 24,  # friday 52 in year 2015
        [0.9] * 24,  # saturday
        [0.9] * 24,  # sunday
    ]
    hourly_value = [0] * 8760
    start_datetime = datetime.datetime(year, 1, 1, 0)
    for i in range(8760):
        current_datetime = start_datetime + datetime.timedelta(hours=i)
        weekday = current_datetime.weekday()
        hour = current_datetime.hour
        hourly_value[i] = week[weekday][hour]
    most_used_schedule = get_most_used_weekday_hourly_schedule(hourly_value, "THURSDAY")
    assert most_used_schedule == [0.4] * 24
