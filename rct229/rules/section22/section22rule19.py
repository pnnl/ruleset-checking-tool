from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
]
REQUIRED_TEMP_RESET = schema_enums["TemperatureResetOptions"]


class Section22Rule19(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule19, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule19.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-19",
            description="The tower shall be controlled to maintain a leaving water temperature, where weather permits.",
            rmr_context="ruleset_model_instances/0",
            list_path="heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11B": ["hvac_sys_11_b"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        temp_reset_type_dict_b = {
            heat_rejection_loop: find_exactly_one_with_field_value(
                "$..fluid_loops[*]", "id", heat_rejection_loop, rmi_b
            )["cooling_or_condensing_design_and_control"]["temperature_reset_type"]
            for heat_rejection_loop in find_all("heat_rejections[*].loop", rmi_b)
        }
        return {"temp_reset_type_dict_b": temp_reset_type_dict_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule19.HeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline
            loop_b = heat_rejection_b["loop"]
            temperature_reset_type = data["temp_reset_type_dict_b"][loop_b]
            return {"temperature_reset_type": temperature_reset_type}

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_reset_type = calc_vals["temperature_reset_type"]
            return temperature_reset_type == REQUIRED_TEMP_RESET.CONSTANT
