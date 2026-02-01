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

    Returns a dictionary mapping each primary chilled water loop id to a list
    of associated secondary loop ids. Primary loops are always returned if
    they are referenced by a chiller, regardless of whether secondary loops
    are present or identifiable.
    """
    baseline_hvac_system_dict = get_baseline_system_types(rmd_b)

    # Loops referenced by chillers → candidate primary loops
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

    # Loops serving non-process CHW coils → candidate secondary loops
    non_process_chw_coil_loop_ids = [
        getattr_(hvac, "hvac system", "cooling_system", "chilled_water_loop")
        for hvac in applicable_hvac_systems
    ]

    primary_secondary_loops_dict: dict[str, list[str]] = {}

    # Iterate through all cooling fluid loops
    for chilled_fluid_loop in find_all(
        f'fluid_loops[*][?(@.type="{FLUID_LOOP.COOLING}")]', rmd_b
    ):
        loop_id = chilled_fluid_loop["id"]

        # Primary loop = referenced by at least one chiller
        if loop_id not in chiller_loop_ids:
            continue

        # Associate secondary loops
        secondary_loop_ids = [
            child_loop["id"]
            for child_loop in chilled_fluid_loop.get("child_loops", [])
            if child_loop["id"] in non_process_chw_coil_loop_ids
        ]

        # Always include the primary loop, even if no secondaries are found
        primary_secondary_loops_dict[loop_id] = secondary_loop_ids

    return primary_secondary_loops_dict
