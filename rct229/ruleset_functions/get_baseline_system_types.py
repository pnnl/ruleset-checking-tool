from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.get_dict_with_terminal_units_and_zones import \
    get_dict_with_terminal_units_and_zones
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_7 import is_baseline_system_7
from rct229.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import \
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys
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
    baseline_hvac_system_dict = {}
    dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
    dict_with_terminal_units_and_zones = get_dict_with_terminal_units_and_zones(rmi_b)

    for hvac_b in find_all("$..heating_ventilation_air_conditioning_systems[*]", rmi_b):
        hvac_b_id = hvac_b["id"]
        terminal_unit_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id]["terminal_unit_list"]
        zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id]["zone_list"]
        # one terminal per zone for all baseline systems
        if all(len(dict_with_terminal_units_and_zones[terminal_id]) == 1 for terminal_id in terminal_unit_id_list):
            system_7 = is_baseline_system_7(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list)
            if system_7 != HVAC_SYS.UNMATCHED:
                # system 7 matched.
                if system_7 not in baseline_hvac_system_dict.keys():
                    baseline_hvac_system_dict[system_7] = []
                baseline_hvac_system_dict[system_7].append(hvac_b_id)
                # added to the dictionary, move to next iteration
                continue

    return baseline_hvac_system_dict

