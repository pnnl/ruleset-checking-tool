import inspect

from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.get_dict_with_terminal_units_and_zones import (
    get_dict_with_terminal_units_and_zones,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_1 import (
    is_baseline_system_1,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_2 import (
    is_baseline_system_2,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_3 import (
    is_baseline_system_3,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_4 import (
    is_baseline_system_4,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_5 import (
    is_baseline_system_5,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_6 import (
    is_baseline_system_6,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_7 import (
    is_baseline_system_7,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_8 import (
    is_baseline_system_8,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_9 import (
    is_baseline_system_9,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_10 import (
    is_baseline_system_10,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_11_1 import (
    is_baseline_system_11_1,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_11_2 import (
    is_baseline_system_11_2,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_12 import (
    is_baseline_system_12,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_13 import (
    is_baseline_system_13,
)
from rct229.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import RCTFailureException
from rct229.utils.jsonpath_utils import find_all


def mock_get_baseline_system_types(rmd):
    # dummy function - more will be added.
    return {"SYS-7A": ["hvac_sys_7_a"], "SYS-11A": ["hvac_sys_11_a"]}


def get_baseline_system_types(rmi_b):
    """
    Identify all the baseline system types modeled in a B-RMD.

    Parameters
    ----------
    rmi_b json The B-RMD that needs to get the list of all HVAC system types.

    Returns dictionary saves all baseline HVAC system types in B-RMD with their IDs
    i.e. {"SYS-3": ["hvac_id_1", "hvac_id_10"], "SYS-7A": ["hvac_id_3", "hvac_id_17", "hvac_id_6], "SYS-9": ["hvac_id_2"]}
    -------
    """

    baseline_system_type_checks = [
        is_baseline_system_1,
        is_baseline_system_2,
        is_baseline_system_3,
        is_baseline_system_4,
        is_baseline_system_5,
        is_baseline_system_6,
        is_baseline_system_7,
        is_baseline_system_8,
        is_baseline_system_9,
        is_baseline_system_10,
        is_baseline_system_11_1,
        is_baseline_system_11_2,
        is_baseline_system_12,
        is_baseline_system_13,
    ]

    # A list of the attribute values from the HVAC_SYS class
    hvac_sys_list = [
        i[1]
        for i in inspect.getmembers(HVAC_SYS)
        if type(i[0]) is str and i[0].startswith("SYS")
    ]

    baseline_hvac_system_dict = {sys_type: [] for sys_type in hvac_sys_list}

    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
    )
    dict_with_terminal_units_and_zones = get_dict_with_terminal_units_and_zones(rmi_b)

    for hvac_b in find_all("$..heating_ventilating_air_conditioning_systems[*]", rmi_b):
        hvac_b_id = hvac_b["id"]
        terminal_unit_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[
            hvac_b_id
        ]["terminal_unit_list"]
        zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id][
            "zone_list"
        ]
        # one terminal per zone for all baseline systems
        if all(
            len(dict_with_terminal_units_and_zones[terminal_id]) == 1
            for terminal_id in terminal_unit_id_list
        ):
            sys_found = False
            for sys_check in baseline_system_type_checks:
                hvac_sys = sys_check(
                    rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list
                )

                if hvac_sys != HVAC_SYS.UNMATCHED:
                    baseline_hvac_system_dict[hvac_sys].append(hvac_b_id)
                    sys_found = True
                    break

            # Add error handling
            if not sys_found:
                hvac_sys_count = len(
                    [
                        hvac_b_id
                        for hvac_sys_key in baseline_hvac_system_dict.keys()
                        if hvac_b_id in baseline_hvac_system_dict[hvac_sys_key]
                    ]
                )
                if hvac_sys_count == 0:
                    raise RCTFailureException(
                        f"Error: HVAC {hvac_b_id} does not match any baseline system type."
                    )
                elif hvac_sys_count > 1:
                    raise RCTFailureException(
                        f"Error: HVAC {hvac_b_id} matches to multiple baseline system types - check your RMD models"
                    )

    return baseline_hvac_system_dict
