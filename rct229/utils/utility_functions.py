from rct229.utils.jsonpath_utils import find_one


def get_max_schedule_multiplier_hourly_value_or_default(rmi, schedule_id, default=None):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_values', rmi
    )
    return hourly_values if hourly_values else default
