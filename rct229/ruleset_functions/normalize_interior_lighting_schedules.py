from rct229.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.utils.assertions import assert_, assert_required_fields, getattr_
from rct229.utils.jsonpath_utils import find_one_with_field_value

# Intended for internal use
from rct229.utils.pint_utils import ZERO, ONE

GET_NORMALIZE_SPACE_SCHEDULE__REQUIRED_FIELDS = {
    "space": {
        "$": ["lighting_space_type", "floor_area"],
        "interior_lighting[*]": ["lighting_multiplier_schedule"],
    }
}


def normalize_interior_lighting_schedules(space, space_height, schedules):
    """This function would determine a normalized schedule for a data element in space.
    NOTE: The function currently only works for interior lighting
    Parameters
    ----------
    space: JSON - The space element that needs to determine a normalized schedule, e.g. space.interior_lighting
    space_height: float, height of a space, it is typically the average height of the thermal zone
    schedules: List[JSON] - schedule element
    Returns
    -------
    A list containing 8760/8784 hourly values of a noralized schedule of the space data element
    """
    assert_required_fields(
        GET_NORMALIZE_SPACE_SCHEDULE__REQUIRED_FIELDS["space"], space
    )

    space_total_power_per_area = 0.0
    space_total_hourly_use_per_area_array = []

    for interior_lighting in space.get("interior_lighting", []):
        power_per_area = interior_lighting.get("power_per_area", ZERO.POWER_PER_AREA) * ONE.POWER_PER_AREA
        # Ensure non-zero power
        assert_(
            power_per_area > ZERO.POWER_PER_AREA,
            f'{interior_lighting["id"]} power_per_area is either missing or set to 0.0',
        )
        space_total_power_per_area += power_per_area

        control_credit = 0.0
        if interior_lighting.get(
            "are_schedules_used_for_modeling_occupancy_control", None
        ):
            control_credit = table_G3_7_lookup(
                lighting_space_type=getattr_(space, "space", "lighting_space_type"),
                # occupancy control type can be None - simply ignored the credit
                occupancy_control_type=interior_lighting.get(
                    "occupancy_control_type", None
                ),
                space_height=space_height,
                space_area=getattr_(space, "space", "floor_area"),
            )["control_credit"]

        schedule_hourly_value = getattr_(
            find_one_with_field_value(
                "$", "id", interior_lighting["lighting_multiplier_schedule"], schedules
            ),
            "schedule",
            "hourly_values",
        )
        hourly_use_per_area_array = [
            # control_credit is a fraction of lighting power density.
            hourly_value / (1.0 - control_credit) * power_per_area
            for hourly_value in schedule_hourly_value
        ]

        if not space_total_hourly_use_per_area_array:
            # if the space_total_hourly_use_per_area_array is empty
            space_total_hourly_use_per_area_array = [0.0] * len(
                hourly_use_per_area_array
            )

        # make sure the hourly schedules have the same number of hours
        assert_(
            len(space_total_hourly_use_per_area_array)
            == len(hourly_use_per_area_array),
            f"Number of hours mismatched. The space has number of hours of: {len(space_total_hourly_use_per_area_array)} "
            f"but the schedule id {interior_lighting['lighting_multiplier_schedule']} has number of hours of: "
            f"{len(hourly_use_per_area_array)}",
        )
        space_total_hourly_use_per_area_array = [
            hourly_value_1 + hourly_value_2
            for hourly_value_1, hourly_value_2 in zip(
                space_total_hourly_use_per_area_array, hourly_use_per_area_array
            )
        ]

    space_normalized_schedule_array = [
        hourly_value / space_total_power_per_area
        for hourly_value in space_total_hourly_use_per_area_array
    ]

    return space_normalized_schedule_array
