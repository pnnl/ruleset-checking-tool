from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entries
from rct229.schema.config import ureg


furnace_capacity_threshold_list = [0, 225000, 99999999]
uh_capacity_threshold_list = [0, 99999999]


def table_G3_5_5_lookup(equipment_type, capacity):
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
            },
            { minimum_efficiency: Quantity - the minimum efficiency rating
              efficiency_metric: str - the metric of the efficiency rating
            }
        ]
    """
    if equipment_type == "Warm-air furnace, gas-fired":
        capacity_threshold_list = furnace_capacity_threshold_list
    else:  # "Warm-air unit heaters, gas-fired"
        capacity_threshold_list = uh_capacity_threshold_list

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

    osstd_entries = find_osstd_table_entries(
        [
            ("equipment_type", equipment_type),
            ("inclusive_minimum_capacity", minimum_capacity.m),
            ("exclusive_maximum_capacity", maximum_capacity.m),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_5"],
    )

    return [
        {key: entry[key] for key in ["minimum_efficiency", "efficiency_metric"]}
        for entry in osstd_entries
    ]
