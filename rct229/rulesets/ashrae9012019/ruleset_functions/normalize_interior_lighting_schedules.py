from rct229.rulesets.ashrae9012019.data_fns.table_G3_7_fns import (
    MANUAL_ON,
    NONE,
    OTHER,
    PARTIAL_AUTO_ON,
    table_G3_7_lookup,
)
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import (
    find_exactly_one_with_field_value,
    find_exactly_required_fields,
)

# Intended for internal use
from rct229.utils.pint_utils import ZERO

GET_NORMALIZE_SPACE_SCHEDULE__REQUIRED_FIELDS = {
    "space": {
        "$": ["lighting_space_type", "floor_area"],
        "interior_lighting[*]": ["lighting_multiplier_schedule"],
    }
}


def normalize_interior_lighting_schedules(
    space: dict,
    space_height: [float | int],
    schedules: list[float | int],
    adjust_for_credit: bool = True,
) -> list[float | int]:
    """This function would determine a normalized schedule for a data element in space.
    NOTE: The function currently only works for interior lighting
    Parameters
    ----------
    space: JSON - The space element that needs to determine a normalized schedule, e.g. space.interior_lighting
    space_height: float, height of a space, it is typically the average height of the thermal zone
    schedules: List[JSON] - schedule element
    adjust_for_credit: Boolean - indicate whether the function needs to adjust schedule value by control credit
    Returns
    -------
    A list containing 8760/8784 hourly values of a normalized schedule of the space data element
    """

    # Implementation note:
    # Because performing arithmetic on 8760-length lists of Pint Quantities is costly,
    # we will pull the units out of the lists. The easiest way to do that is to
    # express each power_per_area value as a number in W/m2.
    # Since the units
    # cancel in the final result, an array of plain numbers can be returned, and the choice
    # of units for power_per_area does not matter.

    find_exactly_required_fields(
        GET_NORMALIZE_SPACE_SCHEDULE__REQUIRED_FIELDS["space"], space
    )

    space_total_power_per_area = 0
    space_total_hourly_use_per_area_array = []

    for interior_lighting in space.get("interior_lighting", []):
        power_per_area = (
            interior_lighting.get("power_per_area", ZERO.POWER_PER_AREA)
            .to("W/m2")
            .magnitude
        )
        # Ensure non-zero power
        assert_(
            power_per_area > 0,
            f'{interior_lighting["id"]} power_per_area is either missing or set to 0.0',
        )
        space_total_power_per_area += power_per_area

        control_credit = 0.0
        if adjust_for_credit and interior_lighting.get(
            "are_schedules_used_for_modeling_occupancy_control", None
        ):
            bonus_adjustment = 1.0
            occupancy_control_type = interior_lighting.get(
                "occupancy_control_type", OTHER
            )

            if occupancy_control_type in [MANUAL_ON, PARTIAL_AUTO_ON]:
                bonus_adjustment = 1.25
            elif occupancy_control_type == NONE:
                # no credit and adjustment for none occupancy control
                bonus_adjustment = 0.0

            control_credit = (
                table_G3_7_lookup(
                    lighting_space_type=getattr_(space, "space", "lighting_space_type"),
                    # occupancy control type can be None - simply ignored the credit
                    space_height=space_height,
                    space_area=getattr_(space, "space", "floor_area"),
                )["control_credit"]
                * bonus_adjustment
            )

        schedule_hourly_value = getattr_(
            find_exactly_one_with_field_value(
                "$[*]",
                "id",
                interior_lighting["lighting_multiplier_schedule"],
                schedules,
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
