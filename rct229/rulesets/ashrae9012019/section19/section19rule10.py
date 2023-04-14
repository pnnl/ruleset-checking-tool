from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

NOT_APPLICABLE_CLIMATE_ZONE = ["CZ0A", "CZ0B", "CZ1A", "CZ1B", "CZ2A", "CZ3A", "CZ4A"]
APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]


class Section19Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule10, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule10.BuildingRule(),
            index_rmr="baseline",
            id="19-10",
            description="Air economizers shall be included in baseline HVAC Systems 3 through 8, and 11, 12, and 13 based on climate as specified in Section G3.1.2.6 with exceptions.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.6 including exceptions 1-3",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        climate_zone = data["climate_zone"]

        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return (climate_zone not in NOT_APPLICABLE_CLIMATE_ZONE) and any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section19Rule10.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
                each_rule=Section19Rule10.BuildingRule.HVACRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(Section19Rule10.BuildingRule.HVACRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def is_applicable(self, context, data=None):
                hvac_b = context.baseline
                hvac_id_b = hvac_b["id"]
                hvac_id_to_flags = data["hvac_id_to_flags"]

                return (
                    hvac_id_to_flags[hvac_id_b]["is_hvac_sys_heating_type_furnace_flag"]
                    or hvac_id_to_flags[hvac_id_b][
                        "is_hvac_sys_heating_type_heat_pump_flag"
                    ]
                    or hvac_id_to_flags[hvac_id_b]["is_hvac_sys_cooling_type_dx_flag"]
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.baseline

                return {}

            def rule_check(self, context, calc_vals=None, data=None):
                return
