from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.schedule_utils import (
    get_max_schedule_multiplier_hourly_value_or_default,
)
from rct229.utils.utility_functions import find_exactly_one_space

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
        total_space_misc_wattage_including_multiplier = sum(
            [
                misc_equip.get("power", ZERO.POWER)
                * max(
                    1.0,
                    get_max_schedule_multiplier_hourly_value_or_default(
                        rmi, misc_equip.get("multiplier_schedule"), 1.0
                    ),
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
