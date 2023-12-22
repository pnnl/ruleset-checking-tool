from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import baseline_system_type_compare
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import get_baseline_system_types

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

DehumidificationOptions = SchemaEnums.schema_enums["DehumidificationOptions"]


class Section23Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule14, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section23Rule14.HVACRule(),
            index_rmr=PROPOSED,
            id="23-14",
            description="If the baseline system does not comply with exceptions in Section 6.5.2.3 then only 25% of the system reheat energy shall be included in the baseline building performance ",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.18 Dehumidification (Systems 3 through 8 and 11, 12, and 13) ",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.PROPOSED
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids
        }

    def list_filter(self, context_item, data):
        hvac_sys_b = context_item.PROPOSED
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return hvac_sys_b["id"] in applicable_hvac_sys_ids