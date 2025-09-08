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
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_3A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_8A,
    HVAC_SYS.SYS_11_1A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A,
    HVAC_SYS.SYS_13A,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
    HVAC_SYS.SYS_1C,
    HVAC_SYS.SYS_3C,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_11_1C,
]
DESIGN_SUPPLY_TEMP = 44 * ureg("degF")


class PRM9012019Rule92r39(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule92r39, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule92r39.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-1",
            description="Baseline chilled water design supply temperature shall be modeled at 44F.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)",
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
        chiller_loop_ids = find_all("chillers[*].cooling_loop", rmd_b)
        return {"loop_chiller_dict": chiller_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        loop_chiller_dict = data["loop_chiller_dict"]
        return fluid_loop_b["id"] in loop_chiller_dict

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule92r39.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "design_supply_temperature"
                    ],
                },
                precision={
                    "design_supply_temperature": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            design_supply_temperature = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["design_supply_temperature"]

            return {
                "design_supply_temperature": CalcQ(
                    "temperature", design_supply_temperature
                ),
                "required_supply_temperature": CalcQ("temperature", DESIGN_SUPPLY_TEMP),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"]
            required_supply_temperature = calc_vals["required_supply_temperature"]

            return self.precision_comparison["design_supply_temperature"](
                design_supply_temperature.to(ureg.kelvin),
                required_supply_temperature.to(ureg.kelvin),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"]
            required_supply_temperature = calc_vals["required_supply_temperature"]
            return std_equal(
                design_supply_temperature.to(ureg.kelvin),
                required_supply_temperature.to(ureg.kelvin),
            )
