from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.is_economizer_modeled_in_proposed import (
    is_economizer_modeled_in_proposed,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one

ClimateZoneOption = SchemaEnums.schema_enums["ClimateZoneOptions2019ASHRAE901"]
AIR_ECONOMIZER = SchemaEnums.schema_enums["AirEconomizerOptions"]
LIGHTING_BUILDING_AREA = SchemaEnums.schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]

NOT_APPLICABLE_CLIMATE_ZONE = [
    ClimateZoneOption.CZ0A,
    ClimateZoneOption.CZ0B,
    ClimateZoneOption.CZ1A,
    ClimateZoneOption.CZ1B,
    ClimateZoneOption.CZ2A,
    ClimateZoneOption.CZ3A,
    ClimateZoneOption.CZ4A,
]
APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

SYSTEM_3_4_TYPES = [HVAC_SYS.SYS_3, HVAC_SYS.SYS_4]


class PRM9012019Rule76q46(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule76q46, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["ruleset_model_descriptions"],
            },
            each_rule=PRM9012019Rule76q46.RulesetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="19-10",
            description="Air economizers shall be included in baseline HVAC Systems 3 through 8, and 11, 12, and 13 based on climate as specified in Section G3.1.2.6 with exceptions."
            "1. Systems that include gas-phase air cleaning to meet the requirements of Standard 62.1, Section 6.1.2. This exception shall be used only if the system in the proposed design does not match the building design."
            "2. Where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems. This exception shall only be used if the system in the proposed design does not use an economizer. If the exception is used, an economizer shall not be included in the baseline building design."
            "3. Systems that serve computer rooms complying with Section G3.1.2.6.1.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.6 including exceptions 1-3",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule76q46.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule76q46.RulesetModelInstanceRule.HVACRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            climate_zone = rmd_b["weather"]["climate_zone"]

            baseline_system_types_dict_b = get_baseline_system_types(rmd_b)

            return climate_zone not in NOT_APPLICABLE_CLIMATE_ZONE and any(
                [
                    baseline_system_types_dict_b[system_type]
                    and baseline_system_type_compare(
                        system_type, applicable_sys_type, False
                    )
                    for system_type in baseline_system_types_dict_b
                    for applicable_sys_type in APPLICABLE_SYS_TYPES
                ]
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            proposed_has_economizer_dict = {}
            for hvac_id_b in find_all(
                f"$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                rmd_b,
            ):
                proposed_has_economizer_dict[
                    hvac_id_b
                ] = is_economizer_modeled_in_proposed(rmd_b, rmd_p, hvac_id_b)

            hvac_system_exception_2_list_b = []
            if find_all("$.buildings[*].refrigerated_cases", rmd_b):
                hvac_system_exception_2_list_b = [
                    hvac_id_b
                    for hvac_id_b in find_all(
                        f'$.buildings[*].building_segments[*][?(@.lighting_building_area_type = "{LIGHTING_BUILDING_AREA.RETAIL}")].heating_ventilating_air_conditioning_systems[*].id',
                        rmd_b,
                    )
                    if not proposed_has_economizer_dict[hvac_id_b]
                ]

            return {
                "hvac_system_exception_2_list_b": hvac_system_exception_2_list_b,
                "HVAC_systems_primarily_serving_comp_rooms_list_b": get_hvac_systems_primarily_serving_comp_room(
                    rmd_b
                ),
                "baseline_system_types_dict_b": get_baseline_system_types(rmd_b),
                "proposed_has_economizer_dict": proposed_has_economizer_dict,
            }

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule76q46.RulesetModelInstanceRule.HVACRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["fan_system"],
                    },
                )

            def is_applicable(self, context, data=None):
                hvac_b = context.BASELINE_0
                hvac_id_b = hvac_b["id"]
                baseline_system_types_dict_b = data["baseline_system_types_dict_b"]
                baseline_system_types_dict_b = {
                    system_type: system_list
                    for system_type, system_list in baseline_system_types_dict_b.items()
                    if system_type in APPLICABLE_SYS_TYPES and system_list
                }

                return any(
                    hvac_id_b in baseline_system_types_dict_b[system_type]
                    for system_type in baseline_system_types_dict_b
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.BASELINE_0
                hvac_id_b = hvac_b["id"]

                baseline_system_types_dict_b = data["baseline_system_types_dict_b"]
                proposed_has_economizer = data["proposed_has_economizer_dict"][
                    hvac_id_b
                ]
                hvac_system_exception_2_list_b = data["hvac_system_exception_2_list_b"]

                HVAC_systems_primarily_serving_comp_rooms_list_b = data[
                    "HVAC_systems_primarily_serving_comp_rooms_list_b"
                ]

                for sys_type, sys_list in baseline_system_types_dict_b.items():
                    if hvac_id_b in baseline_system_types_dict_b[sys_type]:
                        baseline_system_types_b = sys_type

                fan_sys_b = hvac_b["fan_system"]
                fan_air_economizer_b = find_one("$.air_economizer", fan_sys_b)
                fan_air_economizer_type_b = find_one("$.air_economizer.type", fan_sys_b)

                return {
                    "hvac_id_b": hvac_id_b,
                    "baseline_system_types_b": baseline_system_types_b,
                    "fan_air_economizer_b": fan_air_economizer_b,
                    "fan_air_economizer_type_b": fan_air_economizer_type_b,
                    "HVAC_systems_primarily_serving_comp_rooms_list_b": HVAC_systems_primarily_serving_comp_rooms_list_b,
                    "proposed_has_economizer": proposed_has_economizer,
                    "hvac_system_exception_2_list_b": hvac_system_exception_2_list_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                hvac_system_exception_2_list_b = calc_vals[
                    "hvac_system_exception_2_list_b"
                ]
                proposed_has_economizer = calc_vals["proposed_has_economizer"]

                return (
                    # Case 2
                    (
                        (
                            fan_air_economizer_b is None
                            or fan_air_economizer_type_b
                            in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                        )
                        and hvac_id_b in hvac_system_exception_2_list_b
                    )
                    or
                    # Case 4
                    (
                        fan_air_economizer_b is not None
                        and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                        and hvac_id_b in hvac_system_exception_2_list_b
                    )
                    or
                    # Case 6
                    (
                        (
                            fan_air_economizer_b is None
                            or fan_air_economizer_type_b
                            in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                        )
                        and not proposed_has_economizer
                    )
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                hvac_system_exception_2_list_b = calc_vals[
                    "hvac_system_exception_2_list_b"
                ]
                proposed_has_economizer = calc_vals["proposed_has_economizer"]

                if (
                    fan_air_economizer_b is None
                    or fan_air_economizer_type_b
                    in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                ) and hvac_id_b in hvac_system_exception_2_list_b:
                    # Case 2 msg
                    undetermined_msg = (
                        f"Fail unless any of the zones served by the baseline system {hvac_id_b} in the proposed design include supermarket open refrigerated case-work systems that will be affected by "
                        f"using outdoor air for cooling (G3.1.2.6 exception #2)."
                    )
                elif (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and hvac_id_b in hvac_system_exception_2_list_b
                ):
                    # Case 4 msg
                    undetermined_msg = (
                        f"This system {hvac_id_b} appears to meet the criteria associated with Section G3.1.2.6 exception #2 which is that an economizer shall not be modeled in the baseline for systems "
                        f"where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems and the proposed system does not include an economizer. "
                        f"An economizer has been modeled in the baseline when it appears this exception may apply. Manual check recommended."
                    )
                elif (
                    fan_air_economizer_b is None
                    or fan_air_economizer_type_b
                    in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                    and not proposed_has_economizer
                ):
                    # case 6 msg
                    undetermined_msg = (
                        f"Fail unless any of the zones served by the baseline system {hvac_id_b} are served in the proposed design by systems with a gas-phase air cleaning where "
                        f"such air cleaning is requirements of Standard 62.1, Section 6.1.2 (G3.1.2.6 exception #1) or where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems (G3.1.2.6 exception #2)."
                    )

                return undetermined_msg

            def rule_check(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                baseline_system_types_b = calc_vals["baseline_system_types_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                HVAC_systems_primarily_serving_comp_rooms_list_b = calc_vals[
                    "HVAC_systems_primarily_serving_comp_rooms_list_b"
                ]

                return (
                    (
                        fan_air_economizer_b is None
                        or fan_air_economizer_type_b
                        in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                    )
                    and baseline_system_types_b in SYSTEM_3_4_TYPES
                    and hvac_id_b in HVAC_systems_primarily_serving_comp_rooms_list_b
                ) or (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and baseline_system_types_b not in SYSTEM_3_4_TYPES
                    and hvac_id_b
                    not in HVAC_systems_primarily_serving_comp_rooms_list_b
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                baseline_system_types_b = calc_vals["baseline_system_types_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                HVAC_systems_primarily_serving_comp_rooms_list_b = calc_vals[
                    "HVAC_systems_primarily_serving_comp_rooms_list_b"
                ]

                fail_msg = ""
                if (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and baseline_system_types_b in SYSTEM_3_4_TYPES
                    and hvac_id_b in HVAC_systems_primarily_serving_comp_rooms_list_b
                ):
                    # Case 3 msg
                    fail_msg = (
                        f"This system {hvac_id_b} appears to meet the criteria associated with Section G3.1.2.6 exception #3 which is that an economizer shall not be modeled in "
                        f"the baseline for systems that serve computer rooms complying with Section G3.1.2.6.1."
                    )

                return fail_msg
