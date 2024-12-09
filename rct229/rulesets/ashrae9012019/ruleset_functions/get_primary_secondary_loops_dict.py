from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]

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


def get_primary_secondary_loops_dict(rmd_b: dict) -> dict[str, list[str]]:
    """
    Get the list of primary and secondary loops for CHW for a B-RMD.

    Parameters
    ----------
    rmd_b: A baseline ruleset model description

    Returns: primary_secondary_loops_dict
    A dictionary that saves pairs of primary and secondary loops for
    baseline chilled water system, e.g. {primary_loop_1.id: [secondary_loop_1.id,
    secondary_loop2.id], primary_loop_2.id: [secondary_loop3.id]]}. If B-RMD does
    not have primary-secondary loop configuration setup, return an empty dictionary.
    """
    baseline_hvac_system_dict = get_baseline_system_types(rmd_b)

    # Use find_all here to avoid including None for missing cooling_loops
    # Note: a chiller_loop id could appear more than once in this list
    chiller_loop_ids = find_all("$.chillers[*].cooling_loop", rmd_b)

    applicable_hvac_ids = [
        hvac_id
        for sys_type in APPLICABLE_SYS_TYPES
        for hvac_id in baseline_hvac_system_dict[sys_type]
    ]
    applicable_hvac_systems = [
        hvac
        for hvac in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_b,
        )
        if hvac["id"] in applicable_hvac_ids
    ]
    non_process_chw_coil_loop_ids = [
        # Get hvac["cooling_system"]["chilled_water_loop"] or raise exception
        getattr_(hvac, "hvac system", "cooling_system", "chilled_water_loop")
        for hvac in applicable_hvac_systems
    ]
    # Initialize variables
    primary_loops = []
    tmp_primary_secondary_loops_dict = dict()

    # Iterate through cooling type fluid loops
    for chilled_fluid_loop in find_all(
        f'fluid_loops[*][?(@.type="{FLUID_LOOP.COOLING}")]', rmd_b
    ):
        cfl_id = chilled_fluid_loop["id"]
        if cfl_id in chiller_loop_ids and cfl_id in non_process_chw_coil_loop_ids:
            # No loop in baseline shall be primary only
            tmp_primary_secondary_loops_dict = dict()
            primary_loops = []
            break
        elif cfl_id in chiller_loop_ids:
            if all(
                child_loop["id"] in non_process_chw_coil_loop_ids
                for child_loop in getattr_(
                    chilled_fluid_loop, "FluidLoop", "child_loops"
                )
            ):
                primary_loops.append(chilled_fluid_loop)

    for primary_loop in primary_loops:
        tmp_primary_secondary_loops_dict[primary_loop["id"]] = find_all(
            "$.child_loops[*].id", primary_loop
        )
    return tmp_primary_secondary_loops_dict
