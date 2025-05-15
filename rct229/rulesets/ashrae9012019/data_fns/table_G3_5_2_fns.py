from typing import TypedDict, Union

from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    find_osstd_table_entries,
    find_osstd_table_entry,
)


class AppGAirSysEffTableSearchInfo(TypedDict):
    minimum_efficiency: float
    efficiency_metric: str
    most_conservative_efficiency: float | None


class HeatPumpEquipmentType:
    """Enumeration class for equipment types in Table G3.5.2"""

    HEAT_PUMP_AIR_COOLED_HEATING: str = "heat pumps, air-cooled (heating mode)"
    HEAT_PUMP_AIR_COOLED_COOLING: str = "heat pumps, air-cooled (cooling mode)"


class RatingCondition:
    """Enumeration class for rating conditions in Table G3.5.2"""

    SINGLE_PACKAGE: str = "single-package"
    HIGH_TEMP: str = "47F db/43F wb"
    LOW_TEMP: str = "17F db/15F wb"


# Make sure this line is a sorted (ascending order) list
cool_mode_capacity_threshold_list = [0, 65000, 135000, 240000, 999999999]
heat_mode_capacity_threshold_list = [0, 65000, 135000, 999999999]


def table_g3_5_2_lookup(
    equipment_type: str, subcategory_rating_condition: str, capacity: Union[float, int]
) -> AppGAirSysEffTableSearchInfo:
    """Returns the air-cooled heat pump efficiency data based on subcategory/rating condition and capacity
    Parameters
    ----------
    equipment_type : str
        One of the equipment types of the heat pump from table G3.5.2
    subcategory_rating_condition : str
        One of the subcategories or rating conditions of the heat pump from table G3.5.2
    capacity: Union[float, int]
        air conditioner rated capacity in Btu/hr

    Returns
    -------
    dict
        { minimum_efficiency: Quantity - the minimum COP for cooling
          efficiency_metric: str - the efficiency metric
          most_conservative_efficiency: Quantity - the most conservative efficiency
        }
    """

    if equipment_type == HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING:
        capacity_threshold_list = heat_mode_capacity_threshold_list
    elif equipment_type == HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING:
        capacity_threshold_list = cool_mode_capacity_threshold_list
    else:
        raise ValueError(f"Invalid equipment type: {equipment_type}")

    minimum_capacity = min(capacity_threshold_list)
    maximum_capacity = max(capacity_threshold_list)
    for capacity_threshold in capacity_threshold_list:
        if capacity >= capacity_threshold:
            minimum_capacity = capacity_threshold
        if capacity < capacity_threshold:
            maximum_capacity = capacity_threshold
            break

    osstd_entry = find_osstd_table_entry(
        [
            ("equipment_type", equipment_type),
            ("subcategory_rating_condition", subcategory_rating_condition),
            ("inclusive_minimum_capacity", minimum_capacity),
            ("exclusive_maximum_capacity", maximum_capacity),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_2"],
    )

    osstd_type_subcategory_entries = find_osstd_table_entries(
        [
            ("equipment_type", equipment_type),
            ("subcategory_rating_condition", subcategory_rating_condition),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_2"],
    )

    return {
        "minimum_efficiency": osstd_entry["minimum_efficiency"],
        "efficiency_metric": osstd_entry["efficiency_metric"],
        "most_conservative_efficiency": max(
            entry["minimum_efficiency"] for entry in osstd_type_subcategory_entries
        ),
    }
