from typing import List, TypedDict

from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entries


class AppGAirSysEffTableSearchInfo(TypedDict):
    minimum_efficiency: float
    efficiency_metric: str
    most_conservative_efficiency: float | None


class GasHeatingEquipmentType:
    """Enumeration class for equipment types in Table G3.5.5"""

    WARM_AIR_FURNACE_GAS_FIRED: str = "Warm-air furnace, gas-fired"
    WARM_AIR_UNIT_HEATER_GAS_FIRED: str = "Warm-air unit heaters, gas-fired"


furnace_capacity_threshold_list = [0, 225000, 99999999]
uh_capacity_threshold_list = [0, 99999999]


def table_g3_5_5_lookup(
    equipment_type: str, capacity: float
) -> List[AppGAirSysEffTableSearchInfo]:
    """Returns the packaged terminal system efficiency data based on equipment type
    Parameters
    ----------
    equipment_type : str
        One of the equipment types from table G3.5.5
    capacity: quantity
        total heating capacity in Btu/hr

    Returns
    -------
    list
        [
            { minimum_efficiency: Quantity - the minimum efficiency rating
              efficiency_metric: str - the metric of the efficiency rating
              most_conservative_efficiency: None - only included for consistency with other minimum efficiency lookups
            },
            { minimum_efficiency: Quantity - the minimum efficiency rating
              efficiency_metric: str - the metric of the efficiency rating
              most_conservative_efficiency: None - only included for consistency with other minimum efficiency lookups
            }
        ]
    """
    if equipment_type == GasHeatingEquipmentType.WARM_AIR_FURNACE_GAS_FIRED:
        capacity_threshold_list = furnace_capacity_threshold_list
    elif equipment_type == GasHeatingEquipmentType.WARM_AIR_UNIT_HEATER_GAS_FIRED:
        capacity_threshold_list = uh_capacity_threshold_list
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

    osstd_entries = find_osstd_table_entries(
        [
            ("equipment_type", equipment_type),
            ("inclusive_minimum_capacity", minimum_capacity),
            ("exclusive_maximum_capacity", maximum_capacity),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_5"],
    )

    return [
        {
            "minimum_efficiency": entry["minimum_efficiency"],
            "efficiency_metric": entry["efficiency_metric"],
            "most_conservative_efficiency": None,
        }
        for entry in osstd_entries
    ]
