from pydash import flow

from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_space,
    find_exactly_one_schedule,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_, assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, pint_sum

COMPUTER_ROOM_MISC_POWER_DENSITY_THRESHOLD = 20 * ureg("watt/ft2")

LightingSpaceOptions2019ASHRAE901TG37 = schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]

EnergySourceOptions = schema_enums["EnergySourceOptions"]


def is_space_a_computer_room(rmi, space_id):
    space = find_exactly_one_space(rmi, space_id)
    is_space_a_computer_room_flag = (
        space.get("lighting_space_type")
        == LightingSpaceOptions2019ASHRAE901TG37.COMPUTER_ROOM
    )

    if not is_space_a_computer_room_flag:
        # define a function that extracts the max value from an hourly_value schedule.
        get_max_schedule_multiplier_value = flow(
            lambda schedule_id: find_exactly_one_schedule(rmi, schedule_id),
            lambda schedule_obj: schedule_obj.get("hourly_values", [1.0]),
            max,
        )

        total_space_misc_wattage_including_multiplier = pint_sum(
            [
                misc_equip.get("power", ZERO.POWER) * max(
                    1.0,
                    get_max_schedule_multiplier_value(
                        misc_equip.get("multiplier_schedule")
                    )
                    if misc_equip.get("multiplier_schedule")
                    else 1.0
                )
                for misc_equip in find_all("$.miscellaneous_equipment[*]", space)
                if misc_equip.get("energy_type") == EnergySourceOptions.ELECTRICITY
            ],
            ZERO.POWER,
        )

        space_floor_area = getattr_(space, "Space", "floor_area")
        # exception handling if the space has zero floor area
        assert_(space_floor_area > ZERO.AREA, f"Space {space_id} has zero floor area")

        space_epd = total_space_misc_wattage_including_multiplier / space_floor_area
        is_space_a_computer_room_flag = (
            space_epd > COMPUTER_ROOM_MISC_POWER_DENSITY_THRESHOLD
        )

    return is_space_a_computer_room_flag
