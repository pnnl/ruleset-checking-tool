from rct229.utils.jsonpath_utils import find_one


def get_schedule_multiplier_hourly_value_or_default(rmd, schedule_id, default=None):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_values', rmd
    )
    return hourly_values if hourly_values else default


def get_max_schedule_multiplier_hourly_value_or_default(rmd, schedule_id, default=None):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_values', rmd
    )
    return max(hourly_values) if hourly_values else default


def get_max_schedule_multiplier_heating_design_hourly_value_or_default(
    rmd, schedule_id, default=None
):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_heating_design_day', rmd
    )
    return max(hourly_values) if hourly_values else default


def get_max_schedule_multiplier_cooling_design_hourly_value_or_default(
    rmd, schedule_id, default=None
):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_cooling_design_day', rmd
    )
    return max(hourly_values) if hourly_values else default


def get_schedule_year_length(rmd):
    schedules = rmd.get("schedules", [])
    for schedule in schedules:
        hourly_values = schedule.get("hourly_values", [])
        if isinstance(hourly_values, list) and len(hourly_values) > 0:
            return len(hourly_values)
    return 8760
