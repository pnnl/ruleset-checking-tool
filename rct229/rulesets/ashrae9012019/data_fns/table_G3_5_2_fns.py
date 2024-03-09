from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    find_osstd_table_entry,
    find_osstd_table_entries,
)
from rct229.schema.config import ureg


# Make sure this line is a sorted (ascending order) list
cool_mode_capacity_threshold_list = [0, 65000, 135000, 240000, 999999999]
heat_mode_capacity_threshold_list = [0, 65000, 135000, 999999999]


def table_G3_5_2_lookup(equipment_type, subcategory_rating_condition, capacity):
    """Returns the air-cooled heat pump efficiency data based on subcategory/rating condition and capacity
    Parameters
    ----------
    equipment_type : str
        One of the equipment types of the heat pump from table G3.5.2
    subcategory_rating_condition : str
        One of the subcategories or rating conditions of the heat pump from table G3.5.2
    capacity: quantity
        air conditioner rated capacity in Btu/hr

    Returns
    -------
    dict
        { minimum_efficiency: Quantity - the minimum COP for cooling
        }
    """

    if equipment_type == "heat pumps, air-cooled (heating mode)":  # heating mode
        capacity_threshold_list = heat_mode_capacity_threshold_list
    else:  # cooling mode
        capacity_threshold_list = cool_mode_capacity_threshold_list

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
            ("equipment_type", equipment_type),
            ("subcategory_rating_condition", subcategory_rating_condition),
            ("inclusive_minimum_capacity", minimum_capacity.m),
            ("exclusive_maximum_capacity", maximum_capacity.m),
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
