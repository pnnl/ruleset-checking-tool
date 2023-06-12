from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
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
from rct229.utils.jsonpath_utils import find_all, find_one

ClimateZoneOption = schema_enums["ClimateZoneOptions2019ASHRAE901"]
AIR_ECONOMIZER = schema_enums["AirEconomizerOptions"]
LIGHTING_BUILDING_AREA = schema_enums[
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


class Section19Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule10, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather", "ruleset_model_instances"],
                "weather": ["climate_zone"],
            },
            each_rule=Section19Rule10.RulesetModelInstanceRule(),
            index_rmr="baseline",
            id="19-10",
            description="Air economizers shall be included in baseline HVAC Systems 3 through 8, and 11, 12, and 13 based on climate as specified in Section G3.1.2.6 with exceptions."
            "1. Systems that include gas-phase air cleaning to meet the requirements of Standard 62.1, Section 6.1.2. This exception shall be used only if the system in the proposed design does not match the building design."
            "2. Where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems. This exception shall only be used if the system in the proposed design does not use an economizer. If the exception is used, an economizer shall not be included in the baseline building design."
            "3. Systems that serve computer rooms complying with Section G3.1.2.6.1.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.6 including exceptions 1-3",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    def is_applicable(self, context, data=None):
        rmr_b = context.baseline
        rmi_b = rmr_b["ruleset_model_instances"][0]

        baseline_system_types_dict_b = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict_b
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section19Rule10.RulesetModelInstanceRule, self,).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section19Rule10.RulesetModelInstanceRule.HVACRule(),
                index_rmr="baseline",
                list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            )

        def is_applicable(self, context, data=None):
            climate_zone = data["climate_zone"]

            return climate_zone not in NOT_APPLICABLE_CLIMATE_ZONE

        def create_data(self, context, data):
            rmi_b = context.baseline
            rmi_p = context.proposed

            hvac_system_exception_2_list = []
            if find_all("$.refrigerated_casess", rmi_b):
                hvac_system_exception_2_list = [
                    hvac_id_b
                    for hvac_id_b in find_all(
                        f'$.buildings[*].building_segments[*][?(@.lighting_building_area_type = "{LIGHTING_BUILDING_AREA.RETAIL}")].heating_ventilating_air_conditioning_systems[*].id',
                        rmi_b,
                    )
                    if not is_economizer_modeled_in_proposed(rmi_b, rmi_p, hvac_id_b)
                ]

            return {
                "hvac_system_exception_2_list": hvac_system_exception_2_list,
                "HVAC_systems_primarily_serving_comp_rooms_list": get_hvac_systems_primarily_serving_comp_room(
                    rmi_b
                ),
                "baseline_system_types_dict": get_baseline_system_types(rmi_b),
            }

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(Section19Rule10.RulesetModelInstanceRule.HVACRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={
                        "$": ["fan_system"],
                    },
                )

            def is_applicable(self, context, data=None):
                hvac_b = context.baseline
                hvac_id_b = hvac_b["id"]
                baseline_system_types_dict = data["baseline_system_types_dict"]
                baseline_system_types_dict_b = {
                    system_type: system_list
                    for system_type, system_list in baseline_system_types_dict.items()
                    if system_type in APPLICABLE_SYS_TYPES and system_list
                }

                return any(
                    hvac_id_b in baseline_system_types_dict_b[system_type]
                    for system_type in baseline_system_types_dict_b
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.baseline
                hvac_id_b = hvac_b["id"]

                baseline_system_types_dict = data["baseline_system_types_dict"]

                HVAC_systems_primarily_serving_comp_rooms_list = data[
                    "HVAC_systems_primarily_serving_comp_rooms_list"
                ]

                for sys_type, sys_list in baseline_system_types_dict.items():
                    if hvac_id_b in baseline_system_types_dict[sys_type]:
                        baseline_system_types_b = sys_type

                fan_sys_b = hvac_b["fan_system"]
                fan_air_economizer_b = find_one("$.air_economizer", fan_sys_b)
                fan_air_economizer_type_b = find_one("$.air_economizer.type", fan_sys_b)

                return {
                    "hvac_id_b": hvac_id_b,
                    "baseline_system_types_b": baseline_system_types_b,
                    "fan_air_economizer_b": fan_air_economizer_b,
                    "fan_air_economizer_type_b": fan_air_economizer_type_b,
                    "HVAC_systems_primarily_serving_comp_rooms_list": HVAC_systems_primarily_serving_comp_rooms_list,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                hvac_system_exception_2_list = data["hvac_system_exception_2_list"]

                return (
                    (
                        fan_air_economizer_b is None
                        or fan_air_economizer_type_b
                        in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                    )
                    and hvac_id_b in hvac_system_exception_2_list
                ) or (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and hvac_id_b in hvac_system_exception_2_list
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                baseline_system_types_b = calc_vals["baseline_system_types_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                hvac_system_exception_2_list = data["hvac_system_exception_2_list"]

                if (
                    fan_air_economizer_b is None
                    or fan_air_economizer_type_b
                    in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                ) and baseline_system_types_b in hvac_system_exception_2_list:
                    # Case 2 msg
                    undetermined_msg = f"Undetermined unless any of the zones served by the baseline system {hvac_id_b} in the proposed design include supermarket open refrigerated case-work systems that will be affected by using outdoor air for cooling (G3.1.2.6 exception #2)."
                elif (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and hvac_id_b in hvac_system_exception_2_list
                ):
                    # Case 4 msg
                    undetermined_msg = f"This system {hvac_id_b} appears to meet the criteria associated with Section G3.1.2.6 exception #2 which is that an economizer shall not be modeled in the baseline for systems where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems and the proposed system does not include an economizer. An economizer has been modeled in the baseline when it appears this exception may apply. Manual check recommended."

                return undetermined_msg

            def rule_check(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                baseline_system_types_b = calc_vals["baseline_system_types_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                HVAC_systems_primarily_serving_comp_rooms_list = calc_vals[
                    "HVAC_systems_primarily_serving_comp_rooms_list"
                ]
                stop = 1
                return (
                    (
                        fan_air_economizer_b is None
                        or fan_air_economizer_type_b
                        in [None, AIR_ECONOMIZER.FIXED_FRACTION]
                    )
                    and baseline_system_types_b in SYSTEM_3_4_TYPES
                    and hvac_id_b in HVAC_systems_primarily_serving_comp_rooms_list
                ) or (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and baseline_system_types_b not in SYSTEM_3_4_TYPES
                    and hvac_id_b not in HVAC_systems_primarily_serving_comp_rooms_list
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                hvac_id_b = calc_vals["hvac_id_b"]
                baseline_system_types_b = calc_vals["baseline_system_types_b"]
                fan_air_economizer_b = calc_vals["fan_air_economizer_b"]
                fan_air_economizer_type_b = calc_vals["fan_air_economizer_type_b"]
                HVAC_systems_primarily_serving_comp_rooms_list = calc_vals[
                    "HVAC_systems_primarily_serving_comp_rooms_list"
                ]

                if (
                    fan_air_economizer_b is not None
                    and fan_air_economizer_type_b != AIR_ECONOMIZER.FIXED_FRACTION
                    and baseline_system_types_b in SYSTEM_3_4_TYPES
                    and hvac_id_b in HVAC_systems_primarily_serving_comp_rooms_list
                ):
                    # Case 3 msg
                    fail_msg = f"This system {hvac_id_b} appears to meet the criteria associated with Section G3.1.2.6 exception #3 which is that an economizer shall not be modeled in the baseline for systems that serve computer rooms complying with Section G3.1.2.6.1."

                elif (
                    fan_air_economizer_b is None
                    or fan_air_economizer_type_b == AIR_ECONOMIZER.FIXED_FRACTION
                ):
                    # case 6 msg
                    fail_msg = f"Fail unless any of the zones served by the baseline system {hvac_id_b} are served in the proposed design by systems with a gas-phase air cleaning where such air cleaning is requirements of Standard 62.1, Section 6.1.2 (G3.1.2.6 exception #1) or where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems (G3.1.2.6 exception #2)."
                else:
                    fail_msg = ""
                return fail_msg
