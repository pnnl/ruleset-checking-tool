from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg


# Make sure this line is a sorted (ascending order) list
capacity_threshold_list = [0, 65000, 135000, 240000, 760000, 999999999]


def table_G3_5_1_lookup(capacity):
    """Returns the air conditioner efficiency data based on capacity
    Parameters
    ----------
    capacity: quantity
        air conditioner rated capacity in Btu/hr

    Returns
    -------
    dict
        { minimum_efficiency_copnf_cooling: Quantity - the minimum COP for cooling
        }
    """

    # this line converts the list to list of quantities.
    capacity_threshold_list_btuh = list(
        map(lambda ct: ct * ureg("btu_h"), capacity_threshold_list)
    )
    minimum_capacity = min(capacity_threshold_list_btuh)
    maximum_capacity = max(capacity_threshold_list_btuh)
    for capacity_threshold_btuh in capacity_threshold_list_btuh:
        if capacity > capacity_threshold_btuh:
            minimum_capacity = capacity_threshold_btuh
        if capacity < capacity_threshold_btuh:
            maximum_capacity = capacity_threshold_btuh
            break

    osstd_entry = find_osstd_table_entry(
        [
            ("inclusive_minimum_capacity", minimum_capacity.m),
            ("exclusive_maximum_capacity", maximum_capacity.m),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_1"],
    )
    minimum_efficiency_copnf_cooling = osstd_entry["minimum_efficiency_copnf_cooling"]

    return {
        "minimum_efficiency_copnf_cooling": minimum_efficiency_copnf_cooling,
    }
