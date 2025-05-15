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


# Make sure this line is a sorted (ascending order) list
capacity_threshold_list = [0, 65000, 135000, 240000, 760000, 999999999]


def table_g3_5_1_lookup(capacity: Union[float, int]) -> AppGAirSysEffTableSearchInfo:
    """Returns the air conditioner efficiency data based on capacity
    Parameters
    ----------
    capacity: quantity
        air conditioner rated capacity in Btu/hr

    Returns
    -------
    dict
        { minimum_efficiency: Quantity - the minimum COP for cooling
          efficiency_metric: str - the efficiency metric
          most_conservative_efficiency: Quantity - the most conservative efficiency
        }
    """

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
            ("inclusive_minimum_capacity", minimum_capacity),
            ("exclusive_maximum_capacity", maximum_capacity),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_1"],
    )

    osstd_entries = find_osstd_table_entries(
        [],
        osstd_table=data["ashrae_90_1_table_G3_5_1"],
    )

    for entry in osstd_entries:
        assert "minimum_efficiency" in entry and isinstance(
            entry["minimum_efficiency"], (int, float)
        )

    return {
        "minimum_efficiency": osstd_entry["minimum_efficiency"],
        "efficiency_metric": osstd_entry["efficiency_metric"],
        "most_conservative_efficiency": max(
            [entry["minimum_efficiency"] for entry in osstd_entries]
        ),
    }
