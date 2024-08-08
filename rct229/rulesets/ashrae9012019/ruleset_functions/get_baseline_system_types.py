import inspect

from rct229.rule_engine.memoize import memoize
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_1 import (
    is_baseline_system_1,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_2 import (
    is_baseline_system_2,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_3 import (
    is_baseline_system_3,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_4 import (
    is_baseline_system_4,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_5 import (
    is_baseline_system_5,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_6 import (
    is_baseline_system_6,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_7 import (
    is_baseline_system_7,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_8 import (
    is_baseline_system_8,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_9 import (
    is_baseline_system_9,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_10 import (
    is_baseline_system_10,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_11_1 import (
    is_baseline_system_11_1,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_11_2 import (
    is_baseline_system_11_2,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_12 import (
    is_baseline_system_12,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_13 import (
    is_baseline_system_13,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all


@memoize
def get_baseline_system_types(rmd_b: dict) -> dict[HVAC_SYS, list[str]]:
    """
    Identify all the baseline system types modeled in a B-RMD.

    Parameters
    ----------
    rmd_b json The B-RMD that needs to get the list of all HVAC system types.

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
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
    )

    for hvac_b in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd_b,
    ):
        hvac_b_id = hvac_b["id"]
        assert_(
            dict_of_zones_and_terminal_units_served_by_hvac_sys.get(hvac_b_id),
            f"HVAC system {hvac_b_id} is missing in the HeatingVentilatingAiConditioningSystems data group.",
        )

        terminal_unit_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[
            hvac_b_id
        ]["terminal_unit_list"]
        zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id][
            "zone_list"
        ]

        sys_found = False
        for sys_check in baseline_system_type_checks:
            hvac_sys = sys_check(rmd_b, hvac_b_id, terminal_unit_id_list, zone_id_list)

            if hvac_sys != HVAC_SYS.UNMATCHED:
                baseline_hvac_system_dict[hvac_sys].append(hvac_b_id)
                sys_found = True
                # break # TODO: This line must be uncommented before we ship the software. The reason why we commented this line is because an edge case HVAC system could (potentially) match multiple HVAC basseline systems, which require RCT developers to refine the `is_baseline_system` logic.

        assert_(
            sys_found,
            f"Error: HVAC {hvac_b_id} does not match any baseline system type.",
        )

    return baseline_hvac_system_dict
