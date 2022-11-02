from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_primary_secondary_loops_dict import get_primary_secondary_loops_dict
from rct229.utils.jsonpath_utils import find_all


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
PUMP_SPPED_CONTROL = schema_enums["PumpSpeedControlOptions"]



class Section22Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule8.PumpRule(),
            index_rmr="baseline",
            id="22-8",
            description="For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.",
            rmr_context="ruleset_model_instances/0",
            list_path="pumps[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_lists = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(rmi_b)
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        ) and len(primary_secondary_loop_dictionary) != 0

    def create_data(self, context, data):
        rmi_b = context.baseline
        loop_pump_dictionary = {pump["loop_or_piping"]: pump for pump in find_all("pumpss[*]", rmi_b)}

        chw_loop_capacity_dict = {}
        for chiller in find_all("chillers[*]", rmi_b):
            chw_loop_capacity_dict["cooling_loop"] += chiller["rated_capacity"]

        return {"loop_pump_dictionary": loop_pump_dictionary,
                "chw_loop_capacity_dict": chw_loop_capacity_dict}

    class PumpRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule8.PumpRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["range"],
                },
            )

        def get_calc_vals(self, context, data=None):
            pump_b = context.baseline
            secondary_pump = 1

            return {"secondary_pump": secondary_pump}

        def rule_check(self, context, calc_vals=None, data=None):
            secondary_pump = calc_vals["secondary_pump"]

            return secondary_pump["speed_control"]== PUMP_SPPED_CONTROL.VARIABLE_SPEED