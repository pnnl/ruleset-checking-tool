from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]
DESIGN_SUPPLY_TEMP = 180 * ureg("degF")
DESIGN_RETURN_TEMP = 130 * ureg("degF")


class PRM9012019Rule92f56(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule92f56, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule92f56.HeatingFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="21-7",
            description="When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        boiler_loop_ids = find_all("boilers[*].loop", rmd_b)
        return {"loop_boiler_dict": boiler_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        loop_boiler_dict = data["loop_boiler_dict"]
        return fluid_loop_b["id"] in loop_boiler_dict

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule92f56.HeatingFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["heating_design_and_control"],
                    "heating_design_and_control": [
                        "design_supply_temperature",
                        "design_return_temperature",
                    ],
                },
                precision={
                    "design_supply_temperature": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "design_return_temperature": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            design_supply_temperature = fluid_loop_b["heating_design_and_control"][
                "design_supply_temperature"
            ]
            design_return_temperature = fluid_loop_b["heating_design_and_control"][
                "design_return_temperature"
            ]
            return {
                "design_supply_temperature": CalcQ(
                    "temperature", design_supply_temperature
                ),
                "design_return_temperature": CalcQ(
                    "temperature", design_return_temperature
                ),
                "required_supply_temperature": CalcQ("temperature", DESIGN_SUPPLY_TEMP),
                "required_return_temperature": CalcQ("temperature", DESIGN_RETURN_TEMP),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"].to(
                ureg.kelvin
            )
            design_return_temperature = calc_vals["design_return_temperature"].to(
                ureg.kelvin
            )
            required_supply_temperature = calc_vals["required_supply_temperature"].to(
                ureg.kelvin
            )
            required_return_temperature = calc_vals["required_return_temperature"].to(
                ureg.kelvin
            )

            return self.precision_comparison["design_supply_temperature"](
                design_supply_temperature, required_supply_temperature
            ) and self.precision_comparison["design_return_temperature"](
                design_return_temperature, required_return_temperature
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"]
            design_return_temperature = calc_vals["design_return_temperature"]
            required_supply_temperature = calc_vals["required_supply_temperature"]
            required_return_temperature = calc_vals["required_return_temperature"]

            return std_equal(
                design_supply_temperature.to(ureg.kelvin),
                required_supply_temperature.to(ureg.kelvin),
            ) and std_equal(
                design_return_temperature.to(ureg.kelvin),
                required_return_temperature.to(ureg.kelvin),
            )
