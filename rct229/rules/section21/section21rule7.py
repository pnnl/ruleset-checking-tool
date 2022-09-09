from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-1",
    "SYS-5",
    "SYS-7",
    "SYS-11.2",
    "SYS-12",
    "SYS-1A",
    "SYS-7A",
    "SYS-11.2A",
    "SYS-12A",
]
DESIGN_SUPPLY_TEMP = 180 * ureg("degF")
DESIGN_RETURN_TEMP = 130 * ureg("degF")


class Section21Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule7.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-7",
            description="When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        boilers = find_all("$.boilers[*]", rmi_b)
        loop_boiler_dict = {}
        for boiler_b in boilers:
            loop_id = getattr_(boiler_b, "boiler", "loop")
            if not loop_id in loop_boiler_dict.keys():
                loop_boiler_dict[loop_id] = []
            loop_boiler_dict[loop_id].append(boiler_b)
        return {"loop_boiler_dict": loop_boiler_dict}

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7A": ["hvac_sys_7_a"],
            "SYS-12": ["hvac_sys_12"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_boiler_dict = data["loop_boiler_dict"]
        return fluid_loop_b["id"] in loop_boiler_dict.keys()

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule7.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["heating_design_and_control"],
                    "heating_design_and_control": [
                        "design_supply_temperature",
                        "design_return_temperature",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            design_supply_temperature = fluid_loop_b["heating_design_and_control"][
                "design_supply_temperature"
            ]
            design_return_temperature = fluid_loop_b["heating_design_and_control"][
                "design_return_temperature"
            ]
            return {
                "design_supply_temperature": design_supply_temperature,
                "design_return_temperature": design_return_temperature,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"]
            design_return_temperature = calc_vals["design_return_temperature"]
            # return std_equal(
            #     design_supply_temperature, DESIGN_SUPPLY_TEMP
            # ) and std_equal(
            #     design_return_temperature, DESIGN_RETURN_TEMP
            # )

            return (
                design_supply_temperature == DESIGN_SUPPLY_TEMP
                and design_return_temperature == DESIGN_RETURN_TEMP
            )
