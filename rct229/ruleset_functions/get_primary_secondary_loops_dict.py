from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_fluid_loop,
    HVAC_SYS,
)
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

FLUID_LOOP = schema_enums["FluidLoopOptions"]

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]


def get_primary_secondary_loops_dict(rmi_b):
    """
    Get the list of primary and secondary loops for CHW for a B-RMI.

    Parameters
    ----------
    rmi_b: A baseline ruleset model instance

    Returns: primary_secondary_loops_dict
    A dictionary that saves pairs of primary and secondary loops for
    baseline chilled water system, e.g. {primary_loop_1.id: [secondary_loop_1.id,
    secondary_loop2.id], primary_loop_2.id: [secondary_loop3.id]]}. If B-RMI does
    not have primary-secondary loop configuration setup, return an empty dictionary.
    """
    baseline_hvac_system_dict = get_baseline_system_types(rmi_b)

    # Use find_all here to avoid including None for missing cooling_loops
    # Note: a chiller_loop id could appear more than once in this list
    chiller_loop_ids = find_all("$.chillers[*].cooling_loop", rmi_b)

    applicable_hvac_ids = [
        hvac_id
        for sys_type in APPLICABLE_SYS_TYPES
        for hvac_id in baseline_hvac_system_dict[sys_type]
    ]
    applicable_hvac_systems = [
        hvac
        for hvac in find_all(
            "$..building_segments[*].heating_ventilation_air_conditioning_systems[*]",
            rmi_b,
        )
        if hvac["id"] in applicable_hvac_ids
    ]
    non_process_chw_coil_loop_ids = [
        # Get hvac["cooling_system"]["chilled_water_loop"] or raise exception
        getattr_(hvac, "hvac system", "cooling_system", "chilled_water_loop")
        for hvac in applicable_hvac_systems
    ]

    primary_loop_ids = []
    child_loop_ids = []
    secondary_loop_ids = []

    # This flag will be set if the for loop breaks prematurely
    for_break_flag = False
    # Iterate through cooling type fluid loops
    for chilled_fluid_loop in find_all(
        f'fluid_loops[*][?(@.type="{FLUID_LOOP.COOLING}")]', rmi_b
    ):
        cfl_id = chilled_fluid_loop["id"]
        if cfl_id in chiller_loop_ids and cfl_id in non_process_chw_coil_loop_ids:
            for_break_flag = True
            break
        elif cfl_id in chiller_loop_ids:
            if all(
                child_loop_id in non_process_chw_coil_loop_ids
                for child_loop_id in getattr_(
                    chilled_fluid_loop, "FluidLoop", "child_loops"
                )
            ):
                primary_loop_ids.append(cfl_id)
                # NOTE: child_loop_ids could contain duplicates (though it may not make physical sense)
                child_loop_ids = [*child_loop_ids, *chilled_fluid_loop["child_loops"]]
        elif cfl_id in non_process_chw_coil_loop_ids:
            # NOTE: this condition will fail if either child_loops does not exist or
            # if the list is empty
            if chilled_fluid_loop.get("child_loops"):
                for_break_flag = True
                break
            else:
                secondary_loop_ids.append(cfl_id)

    # Use set() to avoid the possibility of duplicates in child_loop_ids
    if for_break_flag or set(child_loop_ids) != set(secondary_loop_ids):
        primary_secondary_loop_dict = {}
    else:
        primary_secondary_loop_dict = {
            primary_loop_id: [
                secondary_loop_id
                for secondary_loop_id in find_exactly_one_fluid_loop(
                    primary_loop_id, rmi_b
                )["child_loops"]
            ]
            for primary_loop_id in primary_loop_ids
        }

    return primary_secondary_loop_dict
