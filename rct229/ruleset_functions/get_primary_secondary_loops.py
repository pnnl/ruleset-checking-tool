from itertools import chain

from rct229.utils.jsonpath_utils import find_all


def get_primary_secondary_loops_dict(rmi_b):
    baseline_hvac_system_dict = get_baseline_system_types(rmi_b)

    # Use find_all here to avoid including None for missing cooling_loop s
    # Note: a chiller_loop id could appear more than once in this list
    chiller_loop_ids = find_all("$.chillers[*].cooling_loop", rmi_b)

    non_process_chw_coil_loop_ids = [hvac.cooling_system.chilled_water_loop]
