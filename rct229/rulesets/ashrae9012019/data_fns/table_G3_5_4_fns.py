from typing import TypedDict

from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry


class AppGAirSysEffTableSearchInfo(TypedDict):
    minimum_efficiency: float
    efficiency_metric: str
    most_conservative_efficiency: float | None


class EquipmentType:
    """Enumeration class for equipment types in Table G3.5.4"""

    PTAC_COOLING: str = "PTAC (cooling mode)"
    PTHP_COOLING: str = "PTHP (cooling mode)"
    PTHP_HEATING: str = "PTHP (heating mode)"


def table_g3_5_4_lookup(equipment_type: str) -> AppGAirSysEffTableSearchInfo:
    """Returns the packaged terminal system efficiency data based on equipment type
    Parameters
    ----------
    equipment_type : str
        One of the equipment types from table G3.5.4

    Returns
    -------
    dict
        { minimum_efficiency: Quantity - the minimum COP
          efficiency_metric: str - the efficiency metric
          most_conservative_efficiency: None - only included for consistency with other minimum efficiency lookups
        }
    """

    osstd_entry = find_osstd_table_entry(
        [
            ("equipment_type", equipment_type),
        ],
        osstd_table=data["ashrae_90_1_table_G3_5_4"],
    )

    return {
        "minimum_efficiency": osstd_entry["minimum_efficiency"],
        "efficiency_metric": osstd_entry["efficiency_metric"],
        "most_conservative_efficiency": None,
    }
