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
from rct229.schema.schema_enums import SchemaEnums

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

PumpSpeedControl = SchemaEnums.schema_enums["PumpSpeedControlOptions"]


class PRM9012019Rule47d94(RuleDefinitionListIndexedBase):
    """Rule 24 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule47d94, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule47d94.PrimaryPumpRule(),
            index_rmd=BASELINE_0,
            id="22-24",
            description="Baseline chilled water loops that do not use purchased chilled water shall have the primary pump modeled as constant volume.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="pumps[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list contains all HVAC systems that are modeled in the rmd_b
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
            and primary_secondary_loop_dict
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        primary_secondary_loops_dict = get_primary_secondary_loops_dict(rmd_b)
        return {"primary_secondary_loops_dict": primary_secondary_loops_dict}

    # filter to only keep loops that have secondary loop(s)
    def list_filter(self, context_item, data):
        pump_b = context_item.BASELINE_0
        primary_loop_ids = data["primary_secondary_loops_dict"]
        return pump_b["loop_or_piping"] in primary_loop_ids

    class PrimaryPumpRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule47d94.PrimaryPumpRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["speed_control"],
                },
            )

        def get_calc_vals(self, context, data=None):
            primary_pump_b = context.BASELINE_0
            primary_pump_speed_control = primary_pump_b["speed_control"]
            return {"primary_pump_speed_control": primary_pump_speed_control}

        def rule_check(self, context, calc_vals=None, data=None):
            primary_pump_speed_control = calc_vals["primary_pump_speed_control"]
            return primary_pump_speed_control == PumpSpeedControl.FIXED_SPEED
