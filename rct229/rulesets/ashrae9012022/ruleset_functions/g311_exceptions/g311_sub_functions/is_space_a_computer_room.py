from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.schedule_utils import (
    get_max_schedule_multiplier_hourly_value_or_default,
)
from rct229.utils.utility_functions import find_exactly_one_space

COMPUTER_ROOM_MISC_POWER_DENSITY_THRESHOLD = 20 * ureg("watt/ft2")

LightingSpaceOptions2019ASHRAE901TG37 = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]
MISCELLANEOUS_EQUIPMENT = SchemaEnums.schema_enums["MiscellaneousEquipmentOptions"]

EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]


def is_space_a_computer_room(rmd: dict, space_id: str) -> bool:
    """
    Returns true or false as to whether space is a computer room. The criteria is such that it is considered a computer room if the total of misc INFORMATION_TECHNOLOGY_EQUIPMENT Power density in W/sf exceeds 20 W/sf per the definition of a computer room in 90.1 Section 3.

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    space_id: str
        space id

    Returns
    -------
    is_space_a_computer_room_flag: bool
        The function returns true or false as to whether space is a computer room. The criteria is such that it is considered a computer room if the total of misc INFORMATION_TECHNOLOGY_EQUIPMENT Power density in W/sf exceeds 20 W/sf per the definition of a computer room in 90.1 Section 3.
    """
    space = find_exactly_one_space(rmd, space_id)
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
                        rmd, misc_equip.get("multiplier_schedule"), 1.0
                    ),
                )
                for misc_equip in find_all("$.miscellaneous_equipment[*]", space)
                if misc_equip.get("energy_type") == EnergySourceOptions.ELECTRICITY
                and misc_equip.get("type")
                == MISCELLANEOUS_EQUIPMENT.INFORMATION_TECHNOLOGY_EQUIPMENT
            ],
            ZERO.POWER,
        )

        space_floor_area = getattr_(space, "spaces", "floor_area")
        # exception handling if the space has zero floor area
        assert_(space_floor_area > ZERO.AREA, f"Space {space_id} has zero floor area")

        space_epd = total_space_misc_wattage_including_multiplier / space_floor_area
        is_space_a_computer_room_flag = (
            space_epd > COMPUTER_ROOM_MISC_POWER_DENSITY_THRESHOLD
        )

    return is_space_a_computer_room_flag
