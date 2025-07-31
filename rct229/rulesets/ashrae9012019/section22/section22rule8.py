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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

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
PUMP_SPEED_CONTROL = SchemaEnums.schema_enums["PumpSpeedControlOptions"]
FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]
MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY = 300.0 * ureg("ton")


class PRM9012019Rule37a05(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule37a05, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule37a05.PrimaryFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-8",
            description="Baseline chilled water systems with a cooling capacity of 300 tons or more shall have the secondary chilled water pump modeled with variable-speed drives.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].fluid_loops[*]",
            precision={
                "chw_loop_capacity": {
                    "precision": 1,
                    "unit": "ton",
                },
            },
        )

    def is_applicable(self, context, data=None):
        rmd_baseline = context.BASELINE_0
        rmd_b = rmd_baseline["ruleset_model_descriptions"][0]
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_list
                ]
            )
            and len(primary_secondary_loop_dict) > 0
        )

    def create_data(self, context, data):
        rmd_baseline = context.BASELINE_0
        rmd_b = rmd_baseline["ruleset_model_descriptions"][0]

        loop_pump_dict = {}
        for pump in find_all("$.pumps[*]", rmd_b):
            if pump["loop_or_piping"] not in loop_pump_dict:
                loop_pump_dict[pump["loop_or_piping"]] = []
            loop_pump_dict[pump["loop_or_piping"]].append(pump)

        chw_loop_capacity_dict = {}
        for chiller in find_all("$.chillers[*]", rmd_b):
            cooling_loop_id = chiller["cooling_loop"]
            if chiller["cooling_loop"] not in chw_loop_capacity_dict:
                chw_loop_capacity_dict[cooling_loop_id] = ZERO.POWER
            chw_loop_capacity_dict[cooling_loop_id] += getattr_(
                chiller, "chiller", "rated_capacity"
            )

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)
        primary_loop_ids = primary_secondary_loop_dict

        return {
            "loop_pump_dict": loop_pump_dict,
            "chw_loop_capacity_dict": chw_loop_capacity_dict,
            "primary_loop_ids": primary_loop_ids,
        }

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        primary_loop_ids = data["primary_loop_ids"]
        chw_loop_capacity_dict = data["chw_loop_capacity_dict"]

        return fluid_loop_b["id"] in primary_loop_ids and (
            chw_loop_capacity_dict[fluid_loop_b["id"]]
            > MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY
            or self.precision_comparison["chw_loop_capacity"](
                chw_loop_capacity_dict[fluid_loop_b["id"]],
                MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY,
            )
        )

    class PrimaryFluidLoopRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule37a05.PrimaryFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule37a05.PrimaryFluidLoopRule.SecondaryChildLoopRule(),
                index_rmd=BASELINE_0,
                list_path="$.child_loops[*]",
            )

        class SecondaryChildLoopRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule37a05.PrimaryFluidLoopRule.SecondaryChildLoopRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    index_rmd=BASELINE_0,
                    each_rule=PRM9012019Rule37a05.PrimaryFluidLoopRule.SecondaryChildLoopRule.PumpTypeRule(),
                )

            def create_context_list(self, context, data=None):
                child_loop_b = context.BASELINE_0
                loop_pump_dict = data["loop_pump_dict"]

                return [
                    produce_ruleset_model_description(
                        USER=None, BASELINE_0=pump_type, PROPOSED=None
                    )
                    for pump_type in loop_pump_dict[child_loop_b["id"]]
                ]

            class PumpTypeRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule37a05.PrimaryFluidLoopRule.SecondaryChildLoopRule.PumpTypeRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                    )

                def get_calc_vals(self, context, data=None):
                    pump_type_b = context.BASELINE_0
                    secondary_pump_speed_control = pump_type_b["speed_control"]

                    return {
                        "secondary_pump_speed_control": secondary_pump_speed_control
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    secondary_pump_speed_control = calc_vals[
                        "secondary_pump_speed_control"
                    ]

                    return (
                        secondary_pump_speed_control
                        == PUMP_SPEED_CONTROL.VARIABLE_SPEED
                    )
