from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)

AIR_SIDE_SYSTEMS_USING_COOLING_SOURCE_OTHER_THAN_PURCHASED_CHILLED_WATER = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]


class Section22Rule40(RuleDefinitionBase):
    """Rule 40 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule40, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            id="22-40",
            description="For systems using purchased chilled water, the cooling source "
            "shall be modeled as purchased chilled water in both the proposed design "
            "and baseline building design. If any system in the proposed design "
            "uses purchased chilled water, all baseline systems with chilled water "
            "coils shall use purchased chilled water. On-site chillers and direct "
            "expansion equipment shall not be modeled in the baseline building design.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmi_p = context.PROPOSED
        purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_p)

        return purchased_chw_hhw_status_dict_p["purchased_cooling"]

    def get_calc_vals(self, context, data=None):
        rmi_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return {"baseline_system_types_dict": baseline_system_types_dict}

    def rule_check(self, context, calc_vals=None, data=None):
        baseline_system_types_dict = calc_vals["baseline_system_types_dict"]
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return not any(
            [
                available_type
                in AIR_SIDE_SYSTEMS_USING_COOLING_SOURCE_OTHER_THAN_PURCHASED_CHILLED_WATER
                for available_type in available_type_list
            ]
        )
