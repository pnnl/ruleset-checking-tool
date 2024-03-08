from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry


def table_G3_5_4_lookup(equipment_type):
    """Returns the packaged terminal system efficiency data based on equipment type
    Parameters
    ----------
    equipment_type : str
        One of the equipment types from table G3.5.4

    Returns
    -------
    dict
        { minimum_efficiency_copnf: Quantity - the minimum COP
        }
    """

    osstd_entry = find_osstd_table_entry(
        [
            ("equipment_type", equipment_type),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_4"],
    )
    minimum_efficiency_copnf = osstd_entry["minimum_efficiency_copnf"]

    return {
        "minimum_efficiency_copnf": minimum_efficiency_copnf,
    }
