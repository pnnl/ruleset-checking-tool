from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hw_loop_zone_list_w_area_dict import (
    get_hw_loop_zone_list_w_area,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_9B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
    HVAC_SYS.SYS_1C,
    HVAC_SYS.SYS_3C,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_11_1C,
]

PUMP_SPEED_CONTROL = schema_enums["PumpSpeedControlOptions"]
PUMP_CONFIGURATION_THRESHOLD = 120_000 * ureg("ft2")


class Section21Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 23 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule10, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule10.PumpRule(),
            index_rmr="baseline",
            id="21-10",
            description="When the building is modeled with HHW plant (served by either boiler(s) or purchased hot "
            "water/steam), the hot water pump shall be modeled as riding the pump curve if the hot water "
            "system serves less than 120,000 ft^2 otherwise it shall be modeled with a VFD.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="pumps[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_types_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_types_list
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        # to avoid pumps in service water heating system
        loop_zone_list_w_area_dict = get_hw_loop_zone_list_w_area(rmi_b)

        return {"loop_zone_list_w_area_dict": loop_zone_list_w_area_dict}

    def list_filter(self, context_item, data):
        pump = context_item.baseline
        loop_zone_list_w_area_dict = data["loop_zone_list_w_area_dict"]
        # filter and select pumps with heating loops (loop_zone_list_w_area_dict keys are heating loops)
        return pump["loop_or_piping"] in loop_zone_list_w_area_dict

    class PumpRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule10.PumpRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False)
            )

        def get_calc_vals(self, context, data=None):
            pump_b = context.baseline
            pump_loop_or_piping_id = pump_b["loop_or_piping"]
            loop_zone_list_w_area_dict = data["loop_zone_list_w_area_dict"]
            total_area = loop_zone_list_w_area_dict[pump_loop_or_piping_id][
                "total_area"
            ]

            target_pump_type = (
                PUMP_SPEED_CONTROL.FIXED_SPEED
                if total_area < PUMP_CONFIGURATION_THRESHOLD
                else PUMP_SPEED_CONTROL.VARIABLE_SPEED
            )

            return {
                "pump_speed_control_type": getattr_(pump_b, "Pump", "speed_control"),
                "target_speed_control_type": target_pump_type,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            pump_speed_control_type = calc_vals["pump_speed_control_type"]
            target_speed_control_type = calc_vals["target_speed_control_type"]
            return pump_speed_control_type == target_speed_control_type
